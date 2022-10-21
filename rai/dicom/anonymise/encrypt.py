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

import base64
import binascii
import hashlib
import json
import os
import re
from typing import List, Set, cast

import cryptography.fernet
import pydicom
import pydicom.datadict
import pydicom.dataelem
import pydicom.tag
from cryptography.hazmat.primitives import hashes as _crypto_hashes
from cryptography.hazmat.primitives import hmac as _crypto_hmac

from . import _identifying, _tags, _typing

TypedDataset = _typing.TypedDataset


class Cipher:
    def __init__(self, key: bytes):
        self._fernet_key, self._search_index_key = _split_key(key=key)
        self._fernet = cryptography.fernet.Fernet(self._fernet_key)

    def encrypt(self, plaintext: bytes):
        token = self._fernet.encrypt(plaintext)

        return token

    def index(self, plaintext: bytes):
        hmac = _crypto_hmac.HMAC(
            key=self._search_index_key, algorithm=_crypto_hashes.SHA224()
        )

        hmac.update(plaintext)
        index_hash = hmac.finalize()

        return index_hash

    def decrypt(self, token: bytes):
        plaintext = self._fernet.decrypt(token)

        return plaintext


def _split_key(key: bytes):
    bytes_key = base64.urlsafe_b64decode(key)

    fernet_key = base64.urlsafe_b64encode(bytes_key[:32])
    search_index_key = bytes_key[32:]

    return fernet_key, search_index_key


def generate_key():
    """Generates a fernet and HMAC key using os.urandom.

    os.urandom is suitable for cryptographic use, see
    https://docs.python.org/3/library/os.html#os.urandom
    """
    # Fernet key [:32]
    # HMAC SHA 224 search index key [32:]
    raw_combined_key = os.urandom(60)
    combined_key = base64.urlsafe_b64encode(raw_combined_key)

    return combined_key


def pseudonymise(
    ds: pydicom.Dataset,
    key: bytes,
):
    grouping = _get_dataset_grouping(ds)

    ds.remove_private_tags()

    cipher = Cipher(key)

    # TODO: Swap this around to instead be 'non-identifying keywords'
    _, non_identifying_tags = _identifying.get_non_identifying()

    encrypted_private_tags_to_store: _typing.PrivateDataStore = dict()

    keywords_encrypted: Set[str] = set()
    keywords_kept: Set[str] = set()
    _recursive_encryption(
        non_identifying_tags=non_identifying_tags,
        cipher=cipher,
        ds=ds,
        parents=tuple([]),
        encrypted_private_tags_to_store=encrypted_private_tags_to_store,
        keywords_encrypted=keywords_encrypted,
        keywords_kept=keywords_kept,
    )

    block = ds.private_block(_tags.TAG_GROUP, _tags.PRIVATE_CREATOR, create=True)

    sequence = []
    for (parents, tag), (
        encrypted_json,
        encrypted_index,
    ) in encrypted_private_tags_to_store.items():
        nested_ds = pydicom.Dataset()
        nested_ds.private_block(_tags.TAG_GROUP, _tags.PRIVATE_CREATOR, create=True)

        parents_sequence = []
        for parent in parents:
            parent_ds = pydicom.Dataset()
            parent_ds.private_block(_tags.TAG_GROUP, _tags.PRIVATE_CREATOR, create=True)

            _tags.add_group(
                ds=parent_ds,
                values={
                    _tags.SEQUENCE_INDEX_TAG: parent.i,
                    _tags.TAG_TAG: parent.tag,
                    _tags.KEYWORD_TAG: pydicom.datadict.keyword_for_tag(parent.tag),
                },
            )
            parents_sequence.append(parent_ds)

        index_sequence = []
        for index in encrypted_index:
            index_ds = pydicom.Dataset()
            index_ds.private_block(_tags.TAG_GROUP, _tags.PRIVATE_CREATOR, create=True)
            _tags.add_new(ds=index_ds, tag=_tags.ENCRYPTED_INDEX_HASH_TAG, value=index)
            index_sequence.append(index_ds)

        _tags.add_group(
            ds=nested_ds,
            values={
                _tags.PARENT_SEQUENCE_TAG: pydicom.Sequence(parents_sequence),
                _tags.TAG_TAG: tag,
                _tags.KEYWORD_TAG: pydicom.datadict.keyword_for_tag(tag),
                _tags.ENCRYPTED_DATA_TAG: encrypted_json,
                _tags.SEARCH_INDEX_SEQUENCE_TAG: pydicom.Sequence(index_sequence),
            },
        )

        sequence.append(nested_ds)

    block.add_new(
        _tags.STORAGE_SEQUENCE_OFFSET,
        _tags.VR_LOOKUP[_tags.STORAGE_SEQUENCE_TAG],
        pydicom.Sequence(sequence),
    )

    if grouping is not None:
        block.add_new(
            _tags.DATASET_GROUPING_OFFSET,
            _tags.VR_LOOKUP[_tags.DATASET_GROUPING_TAG],
            grouping,
        )

    return ds, keywords_encrypted, keywords_kept


def _build_encrypted_index(
    encrypted_index: List[bytes],
    cipher: Cipher,
    data_element: pydicom.DataElement,
):
    if data_element.VR == "SQ":
        data_element = cast(_typing.SequenceDataElement, data_element)
        for ds in data_element.value:
            for nested_data_element in iter(ds):
                _build_encrypted_index(encrypted_index, cipher, nested_data_element)

    else:
        search_index = re.split(r"[\^\s,;_-]", str(data_element.value))

        for item in search_index:
            if item == "":
                continue

            encrypted_index.append(cipher.index(item.lower().encode("utf-8")))


def _recursive_encryption(
    non_identifying_tags: Set[str],
    cipher: Cipher,
    ds: pydicom.Dataset,
    parents: _typing.Parents,
    encrypted_private_tags_to_store: _typing.PrivateDataStore,
    keywords_encrypted: Set[str],
    keywords_kept: Set[str],
):
    for data_element in iter(ds):
        tag = data_element.tag
        keyword = pydicom.datadict.keyword_for_tag(tag)

        # NOTE: By checking that the tag is not within the non_identifying_tags
        # this means that the algorithm is 'fail safe' to new items being
        # added to the DICOM dictionary. Unless it is explicitly declared
        # as non-identifying, all new DICOM dictionary items will by default
        # be assumed to need encryption.
        if tag not in non_identifying_tags:
            keywords_encrypted.add(keyword)

            encrypted_index: List[bytes] = []
            _build_encrypted_index(
                encrypted_index=encrypted_index,
                cipher=cipher,
                data_element=data_element,
            )

            encoded_json_str = data_element.to_json().encode("utf-8")
            data_element.value = data_element.empty_value

            encrypted_json = cipher.encrypt(encoded_json_str)
            encrypted_private_tags_to_store[(parents, tag)] = (
                encrypted_json,
                encrypted_index,
            )
        else:
            keywords_kept.add(keyword)

            if data_element.VR == "SQ":
                data_element = cast(_typing.SequenceDataElement, data_element)

                for i, item in enumerate(data_element.value):
                    _recursive_encryption(
                        non_identifying_tags=non_identifying_tags,
                        cipher=cipher,
                        ds=item,
                        parents=parents + (_typing.Parent(i, data_element.tag),),
                        encrypted_private_tags_to_store=encrypted_private_tags_to_store,
                        keywords_encrypted=keywords_encrypted,
                        keywords_kept=keywords_kept,
                    )


def _get_dataset_grouping(ds: pydicom.Dataset):
    """Generate a hex value in the range of 00 and 0f (inclusive).

    This is irreversibly based upon the patients birth date. That way
    a single patient will always be the same dataset grouping, but this
    grouping value cannot be used in any way to identify the patient.
    """
    birth_date_tag = pydicom.datadict.tag_for_keyword("PatientBirthDate")
    assert isinstance(birth_date_tag, int)

    try:
        data_element = ds[birth_date_tag]
    except KeyError:
        return None

    value: str = data_element.value
    if value == data_element.empty_value:
        return None

    grouping_hash = hashlib.new("sha224")
    grouping_hash.update(value.encode())
    first_hex_letter_of_digest = grouping_hash.hexdigest()[0]
    grouping = binascii.unhexlify("0" + first_hex_letter_of_digest)

    return grouping


def _load_parents(stored_data: TypedDataset):
    parents: _typing.Parents = tuple(
        (
            _typing.Parent(
                i=parent[_tags.SEQUENCE_INDEX_TAG].value,
                tag=parent[_tags.TAG_TAG].value,
            )
            for parent in stored_data[_tags.PARENT_SEQUENCE_TAG].value
        )
    )
    return parents


def _load_tag(stored_data: TypedDataset):
    tag: pydicom.tag.BaseTag = stored_data[_tags.TAG_TAG].value
    return tag


def get_corresponding_data_element(ds: pydicom.Dataset, stored_data: TypedDataset):
    parents = _load_parents(stored_data)
    tag = _load_tag(stored_data)

    for parent in parents:
        ds = ds[parent.tag].value[parent.i]

    data_element = ds[tag]

    return data_element


def restore(
    ds: pydicom.Dataset,
    key: bytes,
):
    cipher = Cipher(key)

    stored_data: _typing.TypedDataset
    for stored_data in ds[_tags.STORAGE_SEQUENCE_TAG].value:
        tag = _load_tag(stored_data)
        encrypted_data: bytes = stored_data[_tags.ENCRYPTED_DATA_TAG].value

        try:
            data_element = get_corresponding_data_element(
                ds=ds, stored_data=stored_data
            )
        except KeyError:
            continue

        decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
        json_dict = json.loads(decrypted_data)
        dataset_json = json.dumps(
            {
                "{:08X}".format(  # pylint: disable = consider-using-f-string
                    tag
                ): json_dict
            }
        )
        decrypted_nested_ds = pydicom.Dataset.from_json(dataset_json)

        assert data_element.VR == decrypted_nested_ds[tag].VR
        assert data_element.value == data_element.empty_value

        data_element.value = decrypted_nested_ds[tag].value

    ds.remove_private_tags()

    return ds


def collect_index(ds: pydicom.Dataset):
    encrypted_index: Set[bytes] = set()
    stored_data: pydicom.Dataset
    for stored_data in ds[_tags.STORAGE_SEQUENCE_TAG].value:
        for index_data in stored_data[_tags.SEARCH_INDEX_SEQUENCE_TAG].value:
            encrypted_index.add(index_data[_tags.ENCRYPTED_INDEX_HASH_TAG].value)

    return encrypted_index


def get_encrypted_index_hash(query: str, key: bytes):
    cipher = Cipher(key)
    index_hash = cipher.index(query.lower().encode("utf-8"))

    return index_hash
