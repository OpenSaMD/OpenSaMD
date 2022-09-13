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

"""Determining the Dice metric"""

import numpy as np
import shapely.geometry
import shapely.geometry.base
from numpy.typing import NDArray


def from_shapely(
    a: shapely.geometry.base.BaseGeometry, b: shapely.geometry.base.BaseGeometry
) -> float:
    """Determine the Dice metric from two shapely geometries.

    Explanation of the Dice is available at:
    <https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient>

    Parameters
    ----------
    a : shapely.geometry.base.BaseGeometry
    b : shapely.geometry.base.BaseGeometry

    Returns
    -------
    float
        The Dice score
    """

    return 2 * a.intersection(b).area / (a.area + b.area)


def from_contours(a: list[NDArray[np.float64]], b: list[NDArray[np.float64]]):
    """Determine the Dice metric from two coordinate lists.

    Explanation of the Dice is available at:
    <https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient>

    Parameters
    ----------
    a : list of (n,2)-ndarrays in row column (y x) order
    b : list of (n,2)-ndarrays in row column (y x) order

    Returns
    -------
    float
        The Dice score
    """
    return from_shapely(
        a=_contours_to_shapely(a),
        b=_contours_to_shapely(b),
    )


def _contours_to_shapely(contours: list[NDArray[np.float64]]):
    geom = shapely.geometry.Polygon()
    for yx_coords in contours:
        xy_coords = np.flip(  # pyright: ignore [reportUnknownMemberType]
            yx_coords, axis=1
        )
        geom = geom.union(shapely.geometry.Polygon(xy_coords))

    return geom
