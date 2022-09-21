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

"""Testing the Dice metric calculations"""

from typing import TypedDict

import numpy as np
import pydicom
import shapely.geometry

from rai.dicom import append

from . import dice

_ContoursOnSlice = list[list[tuple[float, float]]]
_ComparisonSlices = list[tuple[_ContoursOnSlice, _ContoursOnSlice]]


def test_dice_from_dicom():
    """Test the comparison of two DICOM files with the Dice metric"""

    slices: _ComparisonSlices = [
        ([[(0, 0), (0, 1), (1, 1), (1, 0)]], []),
        (
            [[(0, 0), (0, 1), (1, 1), (1, 0)]],
            [[(0, 0), (0, 0.5), (0.5, 0.5), (0.5, 0)]],
        ),
        ([[(0, 0), (0, 1), (1, 1), (1, 0)]], []),
    ]

    a = pydicom.Dataset()
    append.append_dict_to_dataset(
        ds=a,
        to_append={
            "ROIContourSequence": [
                {
                    "ContourSequence": [
                        {
                            "ContourImageSequence": [
                                {
                                    "ReferencedSOPInstanceUID": "",
                                }
                            ],
                            "ContourData": [],
                            "ContourGeometricType": "CLOSED_PLANAR",
                        }
                    ]
                }
            ]
        },
    )


def _create_slice_aligned_dicom_files():
    pass


def test_dice_from_polygons():
    """Compare a range of simple easily calculable dice scores to their
    shapely based equivalent.

    The expected Dice is 2 * intersection_area / sum_of_areas
    """

    cases: list[_PolygonTestCase] = [
        {
            "label": "Two unit squares with 50% overlap",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(0.5, 0), (0.5, 1), (1.5, 1), (1.5, 0)],
            "expected_dice": 2 * 0.5 / (1 + 1),
        },
        {
            "label": "Two unit squares with no overlap",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(1, 0), (1, 1), (1, 1), (1, 0)],
            "expected_dice": 0,
        },
        {
            "label": "Two unit squares with 100% overlap",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "expected_dice": 1,
        },
        {
            "label": "Squares with different area",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(0, 0), (0, 2), (2, 2), (2, 0)],
            "expected_dice": 2 * 1 / (1 + 4),
        },
        {
            "label": "Mirrored concave box-C shapes",
            "a": [(0, 0), (0, 3), (2, 3), (2, 2), (1, 2), (1, 1), (2, 1), (2, 0)],
            "b": [(0, 0), (0, 1), (1, 1), (1, 2), (0, 2), (0, 3), (2, 3), (2, 0)],
            # Creates two C-shapes each with 5 unit square area. The
            # shapes are the mirror of each other. Hence there is no
            # overlap in the middle third, but the top and bottom
            # sections are both intersected.
            "expected_dice": 2 * 4 / (5 + 5),
        },
    ]

    for case in cases:
        a = shapely.geometry.Polygon(case["a"])
        b = shapely.geometry.Polygon(case["b"])

        returned_dice = dice.from_shapely(a, b)

        assert np.abs(returned_dice - case["expected_dice"]) < 0.00001, case["label"]


class _PolygonTestCase(TypedDict):
    label: str
    a: list[tuple[float, float]]
    b: list[tuple[float, float]]
    expected_dice: float
