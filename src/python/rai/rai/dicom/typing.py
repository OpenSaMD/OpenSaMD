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

"""DICOM dataset typing"""

# TODO: Autogenerate this and force it to conform to the DICOM standard
# as detailed within:
# https://github.com/innolitics/dicom-standard/tree/master/standard

from typing import Literal

import pydicom

# pylint: disable = missing-class-docstring


class ContourImageSequenceItem(pydicom.Dataset):
    ReferencedSOPInstanceUID: str


class ContourSequenceItem(pydicom.Dataset):
    ContourImageSequence: list[ContourImageSequenceItem]
    ContourData: list[float]
    ContourGeometricType: Literal[
        "CLOSED_PLANAR", "POINT", "OPEN_PLANAR", "OPEN_NONPLANAR"
    ]


class ROIContourSequenceItem(pydicom.Dataset):
    ContourSequence: list[ContourSequenceItem]


class TypedDataset(pydicom.Dataset):
    ROIContourSequence: list[ROIContourSequenceItem]
