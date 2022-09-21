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

from copy import deepcopy

import pydicom

from .append import append_dict_to_dataset
from .typing import TypedDataset


def run():
    """Dummy docstring"""
    _type_hint_effects()


def _type_hint_effects():
    a = TypedDataset()

    append_dict_to_dataset(
        ds=a,
        to_append={
            "ROIContourSequence": [
                {"ContourSequence": [{"ContourGeometricType": "CLOSED_PLANAR"}]}
            ]
        },
    )

    # Editing the type
    a.ROIContourSequence[0].ContourSequence[0].ContourGeometricType = "OPEN_PLANAR"

    # Editing the type for standard pydicom object
    b = pydicom.Dataset(deepcopy(a))
    b.ROIContourSequence[0].ContourSequence[0].ContourGeometricType = "OPEN_PLANAR"

    # Checking for equality
    assert a == b

    # Without implementing the type checking, any valid CS value can be
    # assigned to this variable without warning
    b.ROIContourSequence[0].ContourSequence[0].ContourGeometricType = "ANYTHING_GOES"
    assert a != b

    print("Everything ran, no errors!")
