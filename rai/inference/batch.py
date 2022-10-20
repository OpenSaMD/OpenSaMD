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

from typing import List, TypeVar

import numpy as np
import tensorflow as tf
import tqdm
from numpy.typing import NDArray

from raicontours import Config

from rai.typing.inference import Points
from rai.vendor.stackoverflow import slicing_without_array_copy

from . import _points

T = TypeVar("T", np.uint8, np.float32)


def create_batch(cfg: Config, points: Points, array_stack: NDArray[T]):
    patch_dimensions = cfg["patch_dimensions"]

    collected_batched_array_stacks: List[NDArray[T]] = []
    for point in points:
        shape = array_stack.shape

        slices: List[slice] = []
        fancy_slices: List[NDArray[np.int64]] = []

        for i in range(3):
            a_slice, _, a_fancy_slice = _points.point_to_indices(
                point[i], merged_size=shape[i], patch_size=patch_dimensions[i]
            )

            slices.append(a_slice)
            fancy_slices.append(a_fancy_slice)

        array_stack_with_slicing = array_stack
        for i in range(3):
            array_stack_with_slicing = slicing_without_array_copy(
                array_stack_with_slicing, slices[i], axis=i
            )

        for i in range(3):
            # Only want to use fancy slicing when absolutely needed, as
            # this results in an array copy (one of the slowest steps of
            # numpy operations)
            if array_stack_with_slicing.shape[i] != patch_dimensions[i]:
                array_stack_with_slicing = array_stack_with_slicing.take(
                    indices=fancy_slices[i], axis=i
                )

        collected_batched_array_stacks.append(array_stack_with_slicing[None, ...])

    array_stack_batched: NDArray[T] = np.concatenate(
        collected_batched_array_stacks, axis=0
    )

    return array_stack_batched


def run_batch(model: tf.keras.Model, model_input, max_batch_size):
    if isinstance(model_input, list):
        steps = int(np.ceil(model_input[0].shape[0] / max_batch_size))

        individual_batches = []
        for item in model_input:
            individual_batches.append(np.array_split(item, steps, axis=0))

        assert len(individual_batches) == len(model_input)

        batches = list(zip(*individual_batches))
    else:
        steps = int(np.ceil(model_input.shape[0] / max_batch_size))
        batches = np.array_split(model_input, steps, axis=0)

    results = []
    for batch in batches:
        results.append(model.predict(batch, verbose=0))

    return np.concatenate(results, axis=0)
