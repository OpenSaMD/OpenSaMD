# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import itertools
import pathlib
from typing import List, Optional, Tuple

import numpy as np
import skimage.measure
import tensorflow as tf
from numpy.typing import NDArray

from raicontours import Config

import rai
from rai.typing.inference import Points

from . import batch as _batch
from . import merge as _merge


def inference_from_dicom_image_paths(
    cfg: Config, image_paths: List[pathlib.Path], max_batch_size
):
    rai_starting_model, rai_dependent_model = rai.load_model(cfg=cfg)

    (
        x_grid,
        y_grid,
        z_grid,
        original_image_stack,
        image_uids,
    ) = rai.paths_to_image_stack_hfs(cfg=cfg, paths=image_paths)

    original_num_slices = original_image_stack.shape[0]

    slice_reduction = cfg["reduce_block_sizes"][0][0]
    desired_num_slices = int(
        np.ceil(original_num_slices / slice_reduction) * slice_reduction
    )

    if original_num_slices != desired_num_slices:
        image_stack = original_image_stack.take(
            range(desired_num_slices), axis=0, mode="clip"
        )
    else:
        image_stack = original_image_stack

    num_slices = image_stack.shape[0]
    assert num_slices == desired_num_slices
    assert image_stack.shape[1:3] == (512, 512)

    reduced_image_stack = skimage.measure.block_reduce(
        image_stack, block_size=cfg["reduce_block_sizes"][0], func=np.mean
    )

    grid = tuple(
        (_get_inference_steps(num_slices) for num_slices in reduced_image_stack.shape)
    )
    predicted_masks = _inference_over_jittered_grid(
        cfg=cfg,
        model=rai_starting_model,
        grid=grid,
        image_stack=reduced_image_stack,
        max_batch_size=max_batch_size,
    )

    for i in range(3):
        predicted_masks = np.repeat(predicted_masks, repeats=2, axis=i)

    assert predicted_masks.shape[0] == image_stack.shape[0]

    reduced_image_stack = skimage.measure.block_reduce(
        image_stack, block_size=cfg["reduce_block_sizes"][1], func=np.mean
    )
    grid = tuple(
        (_get_inference_steps(num_slices) for num_slices in reduced_image_stack.shape)
    )
    predicted_masks = _inference_over_jittered_grid(
        cfg=cfg,
        model=rai_dependent_model,
        grid=grid,
        image_stack=reduced_image_stack,
        masks_stack=predicted_masks,
        max_batch_size=max_batch_size,
    )

    for i in range(1, 3):
        predicted_masks = np.repeat(predicted_masks, repeats=2, axis=i)

    assert predicted_masks.shape[0:3] == image_stack.shape

    grid = tuple((_get_inference_steps(num_slices) for num_slices in image_stack.shape))
    predicted_masks = _inference_over_jittered_grid(
        cfg=cfg,
        model=rai_dependent_model,
        grid=grid,
        image_stack=image_stack,
        masks_stack=predicted_masks,
        max_batch_size=max_batch_size,
    )

    return (
        x_grid,
        y_grid,
        z_grid,
        image_uids,
        original_image_stack,
        predicted_masks[0:original_num_slices, ...],
    )


def _get_inference_steps(num_slices: int):
    # TODO: Reduce this step size
    step_size = 40

    step_size = int(np.ceil(num_slices / np.ceil(num_slices / step_size)))
    inference_steps = list(range(0, num_slices, step_size)) + [num_slices]

    return inference_steps


def _inference_over_jittered_grid(
    cfg: Config,
    model: tf.keras.Model,
    grid: Tuple[List[int], List[int], List[int]],
    image_stack: NDArray[np.float32],
    masks_stack: Optional[NDArray[np.uint8]] = None,
    max_batch_size: Optional[int] = None,
    verify: bool = False,
):
    points = []
    for point in itertools.product(*grid):
        point = np.random.randint(-1, 2, size=3) + point
        points.append(tuple(point.tolist()))

    masks_pd = _patch_inference(
        cfg=cfg,
        model=model,
        points=points,
        image_stack=image_stack,
        masks_stack=masks_stack,
        max_batch_size=max_batch_size,
    )

    if verify:
        where_mask = np.where(masks_pd > 127.5)

        if len(where_mask) > 0:
            min_where_mask = np.min(where_mask, axis=1)
            max_where_mask = np.max(where_mask, axis=1)

            points_array = np.array(points)

            for i in range(3):
                min_point = np.min(points_array[:, i])
                max_point = np.max(points_array[:, i])

                if min_point >= min_where_mask[i] or max_point <= max_where_mask[i]:
                    raise ValueError(
                        "Masks were found outside of the centre points in the "
                        f"provided grid.\nAxis: {i} | "
                        f"Point range: {[min_point, max_point]} | "
                        f"Found mask range: {[min_where_mask[i], max_where_mask[i]]}"
                    )

    return masks_pd


def _patch_inference(
    cfg: Config,
    model: tf.keras.Model,
    points: Points,
    image_stack: NDArray[np.float32],
    masks_stack: Optional[NDArray[np.uint8]] = None,
    max_batch_size: Optional[int] = None,
):
    model_image_input = _batch.create_batch(
        cfg=cfg, points=points, array_stack=image_stack
    )

    useful_points_ref = np.max(model_image_input, axis=(1, 2, 3)) > 0.1
    points = [point for point, useful in zip(points, useful_points_ref) if useful]
    model_image_input = model_image_input[useful_points_ref, ...]

    if masks_stack is not None:
        model_masks_input = _batch.create_batch(
            cfg=cfg, points=points, array_stack=masks_stack
        )

        useful_points_ref = np.max(model_masks_input, axis=(1, 2, 3, 4)) != 0
        points = [point for point, useful in zip(points, useful_points_ref) if useful]

        model_input = [
            model_image_input[useful_points_ref, ...],
            model_masks_input[useful_points_ref, ...],
        ]
    else:
        model_input = model_image_input

    if max_batch_size is not None:
        model_output = _batch.run_batch(
            model=model, model_input=model_input, max_batch_size=max_batch_size
        )
    else:
        model_output = model.predict(model_input)

    num_structures = model.output_shape[-1]

    merged = np.zeros(shape=image_stack.shape + (num_structures,), dtype=np.uint8)
    counts = np.zeros(shape=image_stack.shape + (1,), dtype=np.float32)
    merged, counts = _merge.merge_predictions(
        cfg=cfg, merged=merged, counts=counts, points=points, model_output=model_output
    )

    return merged
