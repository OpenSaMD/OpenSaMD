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
from typing import List, Tuple

import numpy as np
import tensorflow as tf
from numpy.typing import NDArray

from rai.typing.inference import Points

from . import batch as _batch
from . import merge as _merge


def run_inference(
    model: tf.keras.Model, image_stack: NDArray[np.float32], points: Points
):
    model_input = _batch.create_batch(image_stack, points)
    model_output = model.predict(model_input)

    num_structures = model.output_shape[-1]

    merged = np.zeros(shape=image_stack.shape + (num_structures,), dtype=np.uint8)
    counts = np.zeros(shape=image_stack.shape + (1,), dtype=np.float32)
    merged, counts = _merge.merge_predictions(merged, counts, points, model_output)

    return merged


def inference_over_jittered_grid(
    model: tf.keras.Model,
    image_stack: NDArray[np.float32],
    grid: Tuple[List[int], List[int], List[int]],
):
    points = []
    for point in itertools.product(*grid):
        point = np.random.randint(-1, 2, size=3) + point
        points.append(tuple(point.tolist()))

    masks_pd = run_inference(model=model, image_stack=image_stack, points=points)

    where_mask = np.where(masks_pd > 127.5)
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
