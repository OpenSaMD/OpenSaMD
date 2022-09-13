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
import skimage.measure
from numpy.typing import NDArray


def mask_to_contours(
    x_grid: NDArray[np.float64], y_grid: NDArray[np.float64], mask: NDArray[np.uint8]
):
    padded_mask = np.pad(mask, 1)  # pyright: ignore [reportUnknownMemberType]
    contours_coords_padded_image_frame = skimage.measure.find_contours(
        padded_mask, level=127.5
    )
    contours_coords_image_frame = [
        item - 1 for item in contours_coords_padded_image_frame
    ]

    x0, dx = _grid_to_transform(x_grid)
    y0, dy = _grid_to_transform(y_grid)

    contours: list[NDArray[np.float64]] = []
    for yx_coords in contours_coords_image_frame:
        yx_coords[:, 1] = yx_coords[:, 1] * dx + x0
        yx_coords[:, 0] = yx_coords[:, 0] * dy + y0

        contours.append(yx_coords)

    return contours


def contours_to_mask(
    x_grid: NDArray[np.float64],
    y_grid: NDArray[np.float64],
    contours: NDArray[np.float64],
    expansion: int = 16,
):
    expanded_mask = _contours_to_expanded_mask(x_grid, y_grid, contours, expansion)
    float_mask = skimage.measure.block_reduce(
        expanded_mask, block_size=(expansion, expansion), func=np.mean
    )

    mask = np.round(float_mask * 255).astype(np.uint8)

    return mask


def _contours_to_expanded_mask(x_grid, y_grid, contours, expansion):
    mask_size = (len(y_grid), len(x_grid))
    expanded_mask_size = np.array(mask_size) * expansion

    x0, dx = _grid_to_transform(x_grid)
    y0, dy = _grid_to_transform(y_grid)

    expanded_mask = np.zeros(expanded_mask_size)

    for yx_coords in contours:
        y = yx_coords[:, 0]
        x = yx_coords[:, 1]

        i = ((y - y0) / dy) * expansion + (expansion - 1) * 0.5
        j = ((x - x0) / dx) * expansion + (expansion - 1) * 0.5

        expanded_mask = np.logical_or(
            expanded_mask,
            skimage.draw.polygon2mask(expanded_mask_size, np.array(list(zip(i, j)))),
        )

    return expanded_mask


def _grid_to_transform(grid):
    x0 = grid[0]
    all_dx = np.diff(grid)
    dx = all_dx[0]
    assert np.allclose(dx, all_dx)

    return x0, dx
