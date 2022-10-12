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

import collections

from rai.typing.contours import ContoursBySlice, ContoursXY
from rai.typing.dicom import ContourSequenceItem


def get_image_uid_to_contours_map(
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


def contour_sequence_to_contours_by_slice(
    sorted_image_uids: list[str],
    contour_sequence: list[ContourSequenceItem],
) -> ContoursBySlice:
    image_uid_to_contours_map = get_image_uid_to_contours_map(
        contour_sequence=contour_sequence
    )

    contours_by_slice: ContoursBySlice = []

    for image_uid in sorted_image_uids:
        contours = image_uid_to_contours_map[image_uid]
        contours_by_slice.append(contours)

    return contours_by_slice


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
