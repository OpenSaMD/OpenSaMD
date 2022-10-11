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


import numpy as np


def point_to_slices(point_coord, merged_size, patch_size):
    _, indices, _ = point_to_indices(point_coord, merged_size, patch_size)

    merged_first = np.min(indices)
    merged_last = np.max(indices)

    patch_first = np.where(indices == merged_first)[0][-1]
    patch_last = np.where(indices == merged_last)[0][0]

    patch_slice = slice(patch_first, patch_last + 1)
    merged_slice = slice(merged_first, merged_last + 1)

    patch_range = patch_slice.stop - patch_slice.start
    merged_range = merged_slice.stop - merged_slice.start

    assert patch_range == merged_range, f"{patch_range} vs {merged_range}"

    return patch_slice, merged_slice


def point_to_indices(point_coord, merged_size, patch_size):
    half_patch_size = patch_size // 2
    max_value = merged_size - 1

    indices = np.array(
        list(range(point_coord - half_patch_size, point_coord + half_patch_size))
    )
    indices[indices < 0] = 0
    indices[indices > max_value] = max_value

    a_slice = slice(np.min(indices), np.max(indices) + 1)
    offset_indices = indices - a_slice.start

    return a_slice, indices, offset_indices
