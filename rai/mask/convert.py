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

"""Mask conversion to and from contour lines"""

import numpy as np
import skimage.draw
import skimage.measure
from numpy.typing import NDArray

Contours = list[NDArray[np.float64]]
Grid = NDArray[np.float64]
Mask = NDArray[np.uint8]


def mask_to_contours(x_grid: Grid, y_grid: Grid, mask: Mask) -> Contours:
    """Converts a uint8 anti-aliased mask into a series of contours.

    This is a wrapper around `skimage.measure.find_contours` with the
    differences being:

    - A contour that touches the edge of the image will be connected by
      a line that conforms to the image edge
    - Contour points are transformed to the reference frame governed by
      x_grid and y_grid.

    Parameters
    ----------
    x_grid : NDArray[np.float64]
        The x-coordinates of the mask
    y_grid : NDArray[np.float64]
        The y-coordinates of the mask
    mask : NDArray[np.uint8]
        A mask between 0-255 where 0 is outside the contours, 255 inside
        the contours and 1-254 represents a pixel that is partially
        encompassed by the contours.

    Returns
    -------
    contours : list of (n,2)-ndarrays in row column (y x) order
        Each contour is an ndarray of shape (n, 2), consisting of n
        (row, column aka y, x) coordinates along the contour. This is
        inline with the return value of `skimage.measure.find_contours`.

    """

    # The mask is padded so as to force contour closure around the mask
    # edge
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
    x_grid: Grid, y_grid: Grid, contours: Contours, expansion: int = 16
) -> Mask:
    """Creates a uint8 anti-aliased mask from a list of contours.

    Parameters
    ----------
    x_grid : NDArray[np.float64]
        The x-coordinates of the resulting mask
    y_grid : NDArray[np.float64]
        The y-coordinates of the resulting mask
    contours : list of (n,2)-ndarrays in row column (y x) order
        A list of contours where each contour is an ndarray of shape
        (n, 2)
    expansion : int, optional
        The amount to expand the mask by prior to averaging down. The
        default value results in 16 x 16 = 256 possible values for each
        pixel after it has been averaged back to the original size. This
        causes the least amount of information loss when storing the
        resulting mask as a uint8.

    Returns
    -------
    NDArray[np.uint8]
        A mask between 0-255 where 0 is outside the contours, 255 inside
        the contours and 1-254 represents a pixel that is partially
        encompassed by the contours.
    """

    # By creating a binary mask on an expanded grid first, and then
    # shrinking it back down with an np.mean function edge pixels end up
    # being scaled between 0 and 1 based on how much a given pixel is
    # within the contour.
    expanded_mask = _contours_to_expanded_mask(x_grid, y_grid, contours, expansion)
    float_mask = skimage.measure.block_reduce(
        expanded_mask, block_size=(expansion, expansion), func=np.mean
    )

    mask = np.round(  # pyright: ignore [reportUnknownMemberType]
        float_mask * 255
    ).astype(np.uint8)

    return mask


def _contours_to_expanded_mask(
    x_grid: Grid, y_grid: Grid, contours: Contours, expansion: int
):
    expanded_mask_size = (len(y_grid) * expansion, len(x_grid) * expansion)

    x0, dx = _grid_to_transform(x_grid)
    y0, dy = _grid_to_transform(y_grid)

    expanded_mask = np.zeros(expanded_mask_size)

    for yx_coords in contours:
        y = yx_coords[:, 0]
        x = yx_coords[:, 1]

        i = ((y - y0) / dy) * expansion + (expansion - 1) * 0.5
        j = ((x - x0) / dx) * expansion + (expansion - 1) * 0.5

        ij_points = np.concatenate(  # pyright: ignore [reportUnknownMemberType]
            [i[:, None], j[:, None]], axis=-1
        )

        expanded_mask = np.logical_or(
            expanded_mask,
            skimage.draw.polygon2mask(expanded_mask_size, ij_points),
        )

    return expanded_mask


def _grid_to_transform(grid: Grid) -> tuple[float, float]:
    x0 = grid[0]
    all_dx = np.diff(grid)  # pyright: ignore [reportUnknownMemberType]
    dx = all_dx[0]
    assert np.allclose(dx, all_dx)  # pyright: ignore [reportUnknownMemberType]

    return x0, dx
