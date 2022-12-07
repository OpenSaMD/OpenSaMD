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
import pydicom.uid
import shapely.geometry

from rai.dicom import append, uid
from rai.dicom.typing import TypedDataset

from . import dice

_ComparisonSlices = list[tuple[dice.ContoursXY, dice.ContoursXY]]


def test_dice_from_dicom():
    """Test the comparison of two DICOM files with the Dice metric"""

    # TODO: Create more test cases.
    slices: _ComparisonSlices = [
        # Unit square with no overlap on first slice
        ([[(0, 0), (0, 1), (1, 1), (1, 0)]], []),
        # A Unit square for one, and a 0.5 x 0.5 square for the other,
        # with an expected 1/4 overlap.
        (
            [[(0, 0), (0, 1), (1, 1), (1, 0)]],
            [[(0, 0), (0, 0.5), (0.5, 0.5), (0.5, 0)]],
        ),
        # Unit square with no overlap on last slice
        ([[(0, 0), (0, 1), (1, 1), (1, 0)]], []),
    ]

    ds_a, ds_b = _create_slice_aligned_dicom_files(slices)

    a = ds_a.ROIContourSequence[0].ContourSequence
    b = ds_b.ROIContourSequence[0].ContourSequence

    # TODO: Create a `dice.from_dicom()` that returns a dice score per
    # ROI structure. Then test that here instead.
    returned_dice = dice.from_contour_sequence(a, b)

    assert returned_dice == 2 * 0.5 * 0.5 / (0.5 * 0.5 + 1 * 3)


def _create_slice_aligned_dicom_files(slices: _ComparisonSlices):
    """Test utility for aligned contour comparisons.

    Take a list of aligned slice contour coordinates and create two
    DICOM files where the aligned slices have the same
    ReferencedSOPInstanceUID, and therefore the aligned slices within
    the provided list are also aligned between the corresponding DICOM
    pairs.

    """

    contour_sequence_a: list[append.DicomItem] = []
    contour_sequence_b: list[append.DicomItem] = []

    for i, (contours_on_a, contours_on_b) in enumerate(slices):
        reference_sop_instance_uid = pydicom.uid.generate_uid(
            prefix=uid.RAI_CLIENT_ROOT_UID_PREFIX
        )

        for contour in contours_on_a:
            _append_contour_sequence_item(
                contour_sequence=contour_sequence_a,
                reference_sop_instance_uid=reference_sop_instance_uid,
                contour=contour,
                z_value=i,
            )

        for contour in contours_on_b:
            _append_contour_sequence_item(
                contour_sequence=contour_sequence_b,
                reference_sop_instance_uid=reference_sop_instance_uid,
                contour=contour,
                z_value=i,
            )

    a = TypedDataset()
    b = TypedDataset()

    append.append_dict_to_dataset(
        ds=a,
        to_append={"ROIContourSequence": [{"ContourSequence": contour_sequence_a}]},
    )
    append.append_dict_to_dataset(
        ds=b,
        to_append={"ROIContourSequence": [{"ContourSequence": contour_sequence_b}]},
    )

    return a, b


def _append_contour_sequence_item(
    contour_sequence: list[append.DicomItem],
    reference_sop_instance_uid: str,
    contour: dice.ContourXY,
    z_value: float,
):
    contour_sequence.append(
        {
            "ContourImageSequence": [
                {
                    "ReferencedSOPInstanceUID": reference_sop_instance_uid,
                }
            ],
            "ContourData": _contour_to_dicom_format(contour, z_value=z_value),
            "ContourGeometricType": "CLOSED_PLANAR",
        }
    )


def _contour_to_dicom_format(contour: dice.ContourXY, z_value: float):
    dicom_format_contour: list[float] = []
    for x, y in contour:
        dicom_format_contour.extend([x, y, z_value])

    return dicom_format_contour


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
