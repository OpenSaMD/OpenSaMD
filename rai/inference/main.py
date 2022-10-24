# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2021-2022 Radiotherapy AI Holdings Pty Ltd

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
import random
from typing import List, Optional, Tuple, cast

import numpy as np
import skimage.measure
import tensorflow as tf
from numpy.typing import NDArray
from tqdm import tqdm

from raicontours import Config

from rai.typing.inference import Points

from . import batch as _batch
from . import merge as _merge


def inference(cfg: Config, models, image_stack, max_batch_size, step_size: int):
    rai_starting_model, rai_dependent_model = models

    original_num_slices = image_stack.shape[0]

    slice_reduction = cfg["reduce_block_sizes"][0][0]
    desired_num_slices = int(
        np.ceil(original_num_slices / slice_reduction) * slice_reduction
    )

    if original_num_slices != desired_num_slices:
        image_stack = image_stack.take(range(desired_num_slices), axis=0, mode="clip")

    num_slices = image_stack.shape[0]
    assert num_slices == desired_num_slices
    assert image_stack.shape[1:3] == (512, 512)

    reduced_image_stack = skimage.measure.block_reduce(
        image_stack, block_size=cfg["reduce_block_sizes"][0], func=np.mean
    )

    grid = tuple(
        (
            _get_inference_steps(num_slices, step_size)
            for num_slices in reduced_image_stack.shape
        )
    )
    points = _grid_to_jittered_points(grid=grid)

    print(
        "First pass has the image downscaled by "
        f"{cfg['reduce_block_sizes'][0]} with {len(points)} patches centred on the grid:\n"
        f"  z: {grid[0]}\n  y: {grid[1]}\n  x: {grid[2]}"
    )

    predicted_masks, _, _, _ = _inference_over_points(
        cfg=cfg,
        model=rai_starting_model,
        points=points,
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
        (
            _get_inference_steps(num_slices, step_size)
            for num_slices in reduced_image_stack.shape
        )
    )
    print(
        "Second pass has the image downscaled by "
        f"{cfg['reduce_block_sizes'][1]} with {len(points)} patches centred on the grid:\n"
        f"  z: {grid[0]}\n  y: {grid[1]}\n  x: {grid[2]}"
    )

    points = _grid_to_jittered_points(grid=grid)

    predicted_masks, _, _, _ = _inference_over_points(
        cfg=cfg,
        model=rai_dependent_model,
        points=points,
        image_stack=reduced_image_stack,
        masks_stack=predicted_masks,
        max_batch_size=max_batch_size,
    )

    for i in range(1, 3):
        predicted_masks = np.repeat(predicted_masks, repeats=2, axis=i)

    assert predicted_masks.shape[0:3] == image_stack.shape

    grid = tuple(
        (
            _get_inference_steps(num_slices, step_size)
            for num_slices in image_stack.shape
        )
    )
    print(
        "Third pass has no image downscaling with "
        f"{len(points)} patches are centred on the grid:\n"
        f"  z: {grid[0]}\n  y: {grid[1]}\n  x: {grid[2]}"
    )

    points = _grid_to_jittered_points(grid=grid)

    (
        predicted_masks,
        counts,
        min_predictions,
        max_predictions,
    ) = _inference_over_points(
        cfg=cfg,
        model=rai_dependent_model,
        points=points,
        image_stack=image_stack,
        masks_stack=predicted_masks,
        max_batch_size=max_batch_size,
        collect_min_max=True,
    )

    if max_predictions is None or min_predictions is None:
        raise ValueError("Expected max and min predictions here")

    # Estimate of 68% prob interval
    # relevant_points = np.any(
    #     np.logical_and(predicted_masks > 40, predicted_masks < 215), axis=-1
    # )
    # Estimate of 95% prob interval
    relevant_points = np.any(
        np.logical_and(predicted_masks > 6, predicted_masks < 249), axis=-1
    )
    # relevant_points = np.logical_and(
    #     np.any(np.logical_and(predicted_masks > 6, predicted_masks < 249), axis=-1),
    #     counts[..., 0] > 0.5,
    # )
    # TODO: Tune these threshold points.
    # TODO: Consider making the min/max collection be over a reduced
    # range so as to not be biased towards capturing patch edges here.
    # points_with_sufficient_threshold_disagreement = np.any(
    #     np.logical_and(
    #         np.logical_and(max_predictions > 127.5, min_predictions < 127.5),
    #         np.logical_or(max_predictions > 249.0, min_predictions < 6.0),
    #     ),
    #     axis=-1,
    # )

    # 140 was tuned based on the successful smoothing out of
    # checkerboard artefacts on a structure that was "struggling".
    points_with_sufficient_threshold_disagreement = np.any(
        max_predictions - min_predictions > 127.5, axis=-1
    )

    ref_of_points_to_refine = np.logical_and(
        relevant_points, points_with_sufficient_threshold_disagreement
    )

    coords_of_points_to_refine = np.where(ref_of_points_to_refine)
    points = np.vstack(coords_of_points_to_refine).T.tolist()

    random.shuffle(points)

    print(
        "Final pass has no image downscaling with "
        f"{len(points)} pertinent patches chosen."
    )
    predicted_masks, _, _, _ = _inference_over_points(
        cfg=cfg,
        model=rai_dependent_model,
        points=points,
        image_stack=image_stack,
        masks_stack=predicted_masks,
        max_batch_size=max_batch_size,
        merged=predicted_masks,
        counts=counts,
    )

    return predicted_masks[0:original_num_slices, ...]


def _get_inference_steps(num_slices: int, step_size: int):
    step_size = int(np.ceil(num_slices / np.ceil(num_slices / step_size)))
    inference_steps = list(range(0, num_slices, step_size)) + [num_slices]

    return inference_steps


def _grid_to_jittered_points(grid: Tuple[List[int], List[int], List[int]]) -> Points:
    points = []
    for point in itertools.product(*grid):
        point = np.random.randint(-1, 2, size=3) + point
        points.append(tuple(point.tolist()))

    return points


def _inference_over_points(
    cfg: Config,
    model: tf.keras.Model,
    points: Points,
    image_stack: NDArray[np.float32],
    masks_stack: Optional[NDArray[np.uint8]] = None,
    max_batch_size: Optional[int] = None,
    collect_min_max: bool = False,
    merged: Optional[NDArray[np.uint8]] = None,
    counts: Optional[NDArray[np.float32]] = None,
):

    if merged is None:
        num_structures = model.output_shape[-1]
        merged = np.zeros(shape=image_stack.shape + (num_structures,), dtype=np.uint8)

    if counts is None:
        counts = np.zeros(shape=image_stack.shape + (1,), dtype=np.float32)

    min_predictions: Optional[NDArray[np.uint8]]
    max_predictions: Optional[NDArray[np.uint8]]

    if collect_min_max:
        min_predictions = np.array(
            np.ones_like(merged) * 255, dtype=np.uint8, copy=False
        )
        max_predictions = np.zeros_like(merged)
    else:
        min_predictions = None
        max_predictions = None

    max_points = 100
    sections = int(np.ceil(len(points) / max_points))
    split_points = np.array_split(points, sections)
    for a_set_of_points in tqdm(split_points):
        merged, counts, min_predictions, max_predictions = _patch_inference(
            cfg=cfg,
            model=model,
            points=a_set_of_points,
            image_stack=image_stack,
            masks_stack=masks_stack,
            max_batch_size=max_batch_size,
            merged=merged,
            counts=counts,
            min_predictions=min_predictions,
            max_predictions=max_predictions,
        )

    return merged, counts, min_predictions, max_predictions


def _patch_inference(
    cfg: Config,
    model: tf.keras.Model,
    points: Points,
    image_stack: NDArray[np.float32],
    merged: NDArray[np.uint8],
    counts: NDArray[np.float32],
    min_predictions: Optional[NDArray[np.uint8]],
    max_predictions: Optional[NDArray[np.uint8]],
    masks_stack: Optional[NDArray[np.uint8]] = None,
    max_batch_size: Optional[int] = None,
):
    model_image_input = _batch.create_batch(
        cfg=cfg, points=points, array_stack=image_stack
    )

    useful_points_ref = np.max(model_image_input, axis=(1, 2, 3)) > 0.1
    points = [point for point, useful in zip(points, useful_points_ref) if useful]

    if len(points) == 0:
        return merged, counts, min_predictions, max_predictions

    model_image_input = model_image_input[useful_points_ref, ...]

    if masks_stack is not None:
        model_masks_input = _batch.create_batch(
            cfg=cfg, points=points, array_stack=masks_stack
        )

        useful_points_ref = np.max(model_masks_input, axis=(1, 2, 3, 4)) != 0
        points = [point for point, useful in zip(points, useful_points_ref) if useful]

        if len(points) == 0:
            return merged, counts, min_predictions, max_predictions

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

    return _merge.merge_predictions(
        cfg=cfg,
        merged=merged,
        counts=counts,
        points=points,
        model_output=model_output,
        min_predictions=min_predictions,
        max_predictions=max_predictions,
    )
