# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2021-2022 Radiotherapy AI Holdings Pty Ltd

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

from typing import Dict, List, NamedTuple, Tuple, Union, overload

import pydicom
import pydicom.tag

from . import _tags


class Parent(NamedTuple):
    i: int
    tag: pydicom.tag.BaseTag


Parents = Tuple[Parent, ...]
PrivateDataStore = Dict[Tuple[Parents, pydicom.tag.BaseTag], Tuple[bytes, List[bytes]]]


class SequenceDataElement(pydicom.DataElement):
    value: pydicom.Sequence


class BytesDataElement(pydicom.DataElement):
    value: bytes


class TagDataElement(pydicom.DataElement):
    value: pydicom.tag.BaseTag


class StringDataElement(pydicom.DataElement):
    value: str


class IntDataElement(pydicom.DataElement):
    value: int


class TypedDataset(pydicom.Dataset):
    @overload  # type: ignore
    def __getitem__(self, key: slice) -> pydicom.Dataset:
        pass

    @overload
    def __getitem__(self, key: _tags.SequenceTag) -> SequenceDataElement:
        pass

    @overload
    def __getitem__(self, key: _tags.BytesTag) -> BytesDataElement:
        pass

    @overload
    def __getitem__(self, key: _tags.TagTag) -> TagDataElement:
        pass

    @overload
    def __getitem__(self, key: _tags.StringTag) -> StringDataElement:
        pass

    @overload
    def __getitem__(self, key: _tags.IntTag) -> IntDataElement:
        pass

    @overload
    def __getitem__(self, key: pydicom.tag.TagType) -> pydicom.DataElement:
        pass

    def __getitem__(
        self, key: Union[slice, pydicom.tag.TagType]
    ) -> Union[pydicom.Dataset, pydicom.DataElement]:
        return super().__getitem__(key)
