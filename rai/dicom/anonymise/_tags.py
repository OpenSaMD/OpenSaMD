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


from typing import Any, Dict, Tuple, Union, cast

import pydicom
import pydicom.datadict
import pydicom.tag
from typing_extensions import Literal

PRIVATE_CREATOR = "RAi"

TagGroup = Literal[0x49F1]
TAG_GROUP: TagGroup = 0x49F1

Tag = Tuple[TagGroup, int]

STORAGE_SEQUENCE_OFFSET = 0x00
DATASET_GROUPING_OFFSET = 0x80

StorageSequenceTag = Tuple[TagGroup, Literal[0x1000]]
STORAGE_SEQUENCE_TAG = cast(
    StorageSequenceTag, (TAG_GROUP, 0x1000 + STORAGE_SEQUENCE_OFFSET)
)

ParentSequenceTag = Tuple[TagGroup, Literal[0x1010]]
PARENT_SEQUENCE_TAG: ParentSequenceTag = (TAG_GROUP, 0x1010)

SequenceIndexTag = Tuple[TagGroup, Literal[0x1020]]
SEQUENCE_INDEX_TAG: SequenceIndexTag = (TAG_GROUP, 0x1020)

TagTag = Tuple[TagGroup, Literal[0x1030]]
TAG_TAG: TagTag = (TAG_GROUP, 0x1030)

KeywordTag = Tuple[TagGroup, Literal[0x1040]]
KEYWORD_TAG: KeywordTag = (TAG_GROUP, 0x1040)

EncryptedDataTag = Tuple[TagGroup, Literal[0x1050]]
ENCRYPTED_DATA_TAG: EncryptedDataTag = (TAG_GROUP, 0x1050)

SearchIndexSequenceTag = Tuple[TagGroup, Literal[0x1060]]
SEARCH_INDEX_SEQUENCE_TAG: SearchIndexSequenceTag = (TAG_GROUP, 0x1060)

EncryptedIndexHashTag = Tuple[TagGroup, Literal[0x1070]]
ENCRYPTED_INDEX_HASH_TAG = (TAG_GROUP, 0x1070)

DatasetGroupingTag = Tuple[TagGroup, Literal[0x1080]]
DATASET_GROUPING_TAG = cast(
    DatasetGroupingTag, (TAG_GROUP, 0x1000 + DATASET_GROUPING_OFFSET)
)

AssignedDatasetTag = Tuple[TagGroup, Literal[0x1090]]
ASSIGNED_DATASET_TAG: AssignedDatasetTag = (TAG_GROUP, 0x1090)
ASSIGNED_DATASET_OFFSET = 0x90


SequenceTag = Union[StorageSequenceTag, ParentSequenceTag, SearchIndexSequenceTag]
BytesTag = Union[EncryptedDataTag, EncryptedIndexHashTag, DatasetGroupingTag]
StringTag = KeywordTag
IntTag = SequenceIndexTag

VR_LOOKUP = {
    STORAGE_SEQUENCE_TAG: "SQ",
    PARENT_SEQUENCE_TAG: "SQ",
    SEQUENCE_INDEX_TAG: "US",
    TAG_TAG: "AT",
    KEYWORD_TAG: "SH",
    ENCRYPTED_DATA_TAG: "UN",
    SEARCH_INDEX_SEQUENCE_TAG: "SQ",
    ENCRYPTED_INDEX_HASH_TAG: "UN",
    DATASET_GROUPING_TAG: "UN",
    ASSIGNED_DATASET_TAG: "SH",
}

TAG_DESCRIPTIONS = {
    STORAGE_SEQUENCE_TAG: "Encrypted Data Sequence",
    PARENT_SEQUENCE_TAG: "Parent Sequence",
    SEQUENCE_INDEX_TAG: "Index",
    TAG_TAG: "Tag",
    KEYWORD_TAG: "Keyword",
    ENCRYPTED_DATA_TAG: "Data",
    SEARCH_INDEX_SEQUENCE_TAG: "Search Index Sequence",
    ENCRYPTED_INDEX_HASH_TAG: "Hash",
    DATASET_GROUPING_TAG: "Dataset Grouping",
    ASSIGNED_DATASET_TAG: "Assigned Dataset",
}


def add_group(ds: pydicom.Dataset, values: Dict[Tag, Any]):
    for tag, value in values.items():
        add_new(ds=ds, tag=tag, value=value)


def add_new(ds: pydicom.Dataset, tag: Tag, value):
    vr = VR_LOOKUP[tag]
    ds.add_new(tag=tag, VR=vr, value=value)


def add_tags_to_pydicom():
    new_dict_items = {
        tag_format(tag): (vr, "3", TAG_DESCRIPTIONS[tag])
        for tag, vr in VR_LOOKUP.items()
    }
    pydicom.datadict.add_private_dict_entries(PRIVATE_CREATOR, new_dict_items)


def tag_format(tag: Tuple[int, int]):
    return tag[0] * 0x10000 + tag[1]
