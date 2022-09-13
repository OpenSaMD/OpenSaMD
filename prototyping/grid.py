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

"""Grid conversion to and from image transform parameters"""

from typing import NamedTuple, TypedDict

import numpy as np
from numpy.typing import NDArray


class Coordinates2D(NamedTuple):
    """Floating point 2D coordinates"""

    x: float
    y: float


class Size2D(NamedTuple):
    """Integer xy dimensions"""

    x: int
    y: int


GridItem = NDArray[np.float64]


class Grid(NamedTuple):
    """A 2D image grid"""

    x: GridItem
    y: GridItem


class TransformParameters(TypedDict):
    """Image transform parameters"""

    spacing: Coordinates2D
    start: Coordinates2D
    sign: Coordinates2D
    size: Size2D


def transform_parameters_to_grid(transform: TransformParameters) -> Grid:
    """Creates an equally spaced grid when provided image transform parameters"""

    dx, dy = transform["spacing"]
    x0, y0 = transform["start"]
    x_sign, y_sign = transform["sign"]
    x_length, y_length = transform["size"]

    x_grid = np.linspace(x0, x0 + (x_length - 1) * dx * x_sign, x_length)
    y_grid = np.linspace(y0, y0 + (y_length - 1) * dy * y_sign, y_length)

    grid = Grid(x_grid, y_grid)

    return grid


class _TransformItem(TypedDict):
    spacing: float
    start: float
    sign: float
    size: int


class _TransformItems(NamedTuple):
    x: _TransformItem
    y: _TransformItem


def grid_to_transform_parameters(grid: Grid) -> TransformParameters:
    """Converts 2D image grid to image transform parameters"""

    transformed: list[_TransformItem] = [
        _single_grid_to_transform_item(grid_item) for grid_item in grid
    ]

    items = _TransformItems(transformed[0], transformed[1])

    transform_parameters: TransformParameters = {
        "spacing": Coordinates2D(items.x["spacing"], items.y["spacing"]),
        "start": Coordinates2D(items.x["start"], items.y["start"]),
        "sign": Coordinates2D(items.x["sign"], items.y["sign"]),
        "size": Size2D(items.x["size"], items.y["size"]),
    }

    return transform_parameters


def _single_grid_to_transform_item(grid_item: GridItem) -> _TransformItem:
    start = grid_item[0]

    all_diff = np.diff(grid_item)  # pyright: ignore [reportUnknownMemberType]
    diff_0 = all_diff[0]
    if not np.allclose(diff_0, all_diff):  # pyright: ignore [reportUnknownMemberType]
        raise ValueError("Expected all grid spacing items to be equal")

    sign = diff_0 / np.abs(diff_0)
    assert sign in (1, -1)

    spacing = diff_0 / sign
    assert spacing == np.abs(diff_0)

    size = len(grid_item)

    transform_item: _TransformItem = {
        "spacing": spacing,
        "start": start,
        "sign": sign,
        "size": size,
    }

    return transform_item
