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

import shapely.geometry
import shapely.geometry.base

from rai.dicom import structures as _dicom_structures
from rai.typing.contours import ContoursBySlice, ContoursXY
from rai.typing.dicom import ContourSequenceItem


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
    image_uids_to_contours_a = _dicom_structures.get_image_uid_to_contours_map(a)
    image_uids_to_contours_b = _dicom_structures.get_image_uid_to_contours_map(b)

    all_image_uids = set(image_uids_to_contours_a.keys()).union(
        image_uids_to_contours_b.keys()
    )

    contours_by_slice_a: ContoursBySlice = []
    contours_by_slice_b: ContoursBySlice = []
    for image_uid in all_image_uids:
        contours_by_slice_a.append(image_uids_to_contours_a[image_uid])
        contours_by_slice_b.append(image_uids_to_contours_b[image_uid])

    return from_contours_by_slice(a=contours_by_slice_a, b=contours_by_slice_b)


def from_contours_by_slice(a: ContoursBySlice, b: ContoursBySlice):
    assert len(a) == len(b)

    intersection_area = 0
    total_area = 0
    for contours_a, contours_b in zip(a, b):
        shapley_a = _contours_xy_to_shapely(contours_a)
        shapely_b = _contours_xy_to_shapely(contours_b)

        intersection_area += shapley_a.intersection(shapely_b).area
        total_area += shapley_a.area + shapely_b.area

    return 2 * intersection_area / total_area


def _contours_xy_to_shapely(contours: ContoursXY):
    geom = shapely.geometry.Polygon()
    for xy_coords in contours:
        geom = geom.union(shapely.geometry.Polygon(xy_coords))

    return geom


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


def from_contours(a: ContoursXY, b: ContoursXY):
    """Determine the Dice metric from two coordinate lists.

    The Dice score is an overlap metric where a value of 1 indicates
    100% overlap, and a value of 0 indicates 0% overlap.

    Further explanation of the Dice is available at:
    <https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient>

    Parameters
    ----------
    a : ContoursXY
        A list of contours where each contour is a list of points in
        (x, y) order.
    b : ContoursXY
        A list of contours where each contour is a list of points in
        (x, y) order.

    Returns
    -------
    float
        The Dice score
    """
    return from_shapely(
        a=_contours_yx_to_shapely(a),
        b=_contours_yx_to_shapely(b),
    )


def _contours_yx_to_shapely(contours: ContoursXY):
    geom = shapely.geometry.Polygon()
    for xy_coords in contours:
        geom = geom.union(shapely.geometry.Polygon(xy_coords))

    return geom
