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

import collections

import numpy as np
import shapely.geometry
import shapely.geometry.base
from numpy.typing import NDArray

from rai.dicom.typing import ContourSequenceItem

ContourXY = list[tuple[float, float]]
ContoursXY = list[ContourXY]


def from_contour_sequence(a: list[ContourSequenceItem], b: list[ContourSequenceItem]):
    """Determine the Dice metric between two DICOM Contour Sequences.

    The Dice score is an overlap metric where a value of 1 indicates
    100% overlap, and a value of 0 indicates 0% overlap.

    Further explanation of the Dice is available at:
    <https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient>

    Parameters
    ----------
    a : pydicom.Sequence
    b : pydicom.Sequence

    Returns
    -------
    float
        The Dice score
    """
    image_uids_to_contours_a = _get_image_uid_to_contours_map(a)
    image_uids_to_contours_b = _get_image_uid_to_contours_map(b)

    all_image_uids = set(image_uids_to_contours_a.keys()).union(
        image_uids_to_contours_b.keys()
    )

    intersection_area = 0
    total_area = 0
    for image_uid in all_image_uids:
        shapley_a = _contours_xy_to_shapely(image_uids_to_contours_a[image_uid])
        shapely_b = _contours_xy_to_shapely(image_uids_to_contours_b[image_uid])

        intersection_area += shapley_a.intersection(shapely_b).area
        total_area += shapley_a.area + shapely_b.area

    return 2 * intersection_area / total_area


def _contours_xy_to_shapely(contours: ContoursXY):
    geom = shapely.geometry.Polygon()
    for xy_coords in contours:
        geom = geom.union(shapely.geometry.Polygon(xy_coords))

    return geom


def _get_image_uid_to_contours_map(
    contour_sequence: list[ContourSequenceItem],
):
    image_uid_to_contours_map: dict[str, ContoursXY] = collections.defaultdict(list)

    for item in contour_sequence:
        contour_image_sequence = item.ContourImageSequence

        assert len(contour_image_sequence) == 1
        contour_image_sequence_item = contour_image_sequence[0]

        referenced_image_uid = contour_image_sequence_item.ReferencedSOPInstanceUID

        assert item.ContourGeometricType == "CLOSED_PLANAR"

        image_uid_to_contours_map[referenced_image_uid].append(
            _convert_dicom_contours(item.ContourData)
        )

    return image_uid_to_contours_map


def _convert_dicom_contours(contour_data: list[float]):
    x = contour_data[0::3]
    y = contour_data[1::3]
    z = contour_data[2::3]

    assert len(x) == len(y)
    assert len(x) == len(z)

    # Co-planar
    assert len(set(z)) == 1

    contours = list(zip(x, y))

    return contours


def from_shapely(
    a: shapely.geometry.base.BaseGeometry, b: shapely.geometry.base.BaseGeometry
) -> float:
    """Determine the Dice metric from two shapely geometries.

    The Dice score is an overlap metric where a value of 1 indicates
    100% overlap, and a value of 0 indicates 0% overlap.

    Further explanation of the Dice is available at:
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


# TODO: Conform to either ContoursYX or ContoursXY internally within
# rai. Don't swap between using both within the function APIs.
ContourYX = NDArray[np.float64]
ContoursYX = list[ContourYX]


def from_contours(a: ContoursYX, b: ContoursYX):
    """Determine the Dice metric from two coordinate lists.

    The Dice score is an overlap metric where a value of 1 indicates
    100% overlap, and a value of 0 indicates 0% overlap.

    Further explanation of the Dice is available at:
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
        a=_contours_yx_to_shapely(a),
        b=_contours_yx_to_shapely(b),
    )


def _contours_yx_to_shapely(contours: ContoursYX):
    geom = shapely.geometry.Polygon()
    for yx_coords in contours:
        xy_coords = np.flip(  # pyright: ignore [reportUnknownMemberType]
            yx_coords, axis=1
        )
        geom = geom.union(shapely.geometry.Polygon(xy_coords))

    return geom
