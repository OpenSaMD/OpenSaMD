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

"""DICOM UID constants and tools"""

import functools
import re
import secrets
import uuid
from typing import Optional, Union

import pydicom
import pydicom.uid

from rai._version import __version__, version_info

# Many thanks to the Medical Connections for offering free
# valid UIDs (http://www.medicalconnections.co.uk/FreeUID.html)
# Their service was used to obtain the following root UID for
# Radiotherapy AI:
_RAI_ROOT_UID_PREFIX = "1.2.826.0.1.3680043.10.756."

_RAI_INTERNAL_ROOT_UID_PREFIX = f"{_RAI_ROOT_UID_PREFIX}0."
_RAI_CLIENT_ROOT_UID_PREFIX = f"{_RAI_ROOT_UID_PREFIX}1."

_RAI_CONTOURS_PRODUCT_ID = "1"

RAI_IMPLEMENTATION_VERSION_NAME = f"rai-v{__version__}"
# http://dicom.nema.org/medical/dicom/current/output/chtml/part07/sect_D.3.3.2.4.html
assert len(RAI_IMPLEMENTATION_VERSION_NAME) <= 16

# TODO: Add a representation within the implementation uid of production
# vs dev release.
_NO_DEV_VERSION = ".".join([str(item) for item in version_info[0:3]])

RAI_CONTOURS_IMPLEMENTATION_CLASS_UID = (
    f"{_RAI_INTERNAL_ROOT_UID_PREFIX}{_RAI_CONTOURS_PRODUCT_ID}.{_NO_DEV_VERSION}"
)

assert re.match(
    pydicom.uid.RE_VALID_UID, RAI_CONTOURS_IMPLEMENTATION_CLASS_UID
), RAI_CONTOURS_IMPLEMENTATION_CLASS_UID


# https://github.com/pydicom/pynetdicom/blob/9e8a86d70149e2a23ba2492b705165bf24fc7bdb/pynetdicom/sop_class.py#L390
RT_STRUCTURE_SET_STORAGE_UID = "1.2.840.10008.5.1.4.1.1.481.3"
CT_IMAGE_STORAGE_UID = "1.2.840.10008.5.1.4.1.1.2"
RT_PLAN_STORAGE_UID = "1.2.840.10008.5.1.4.1.1.481.5"
RT_DOSE_STORAGE_UID = "1.2.840.10008.5.1.4.1.1.481.2"

ALL_STORAGE_UIDS = [
    RT_STRUCTURE_SET_STORAGE_UID,
    CT_IMAGE_STORAGE_UID,
    RT_PLAN_STORAGE_UID,
    RT_DOSE_STORAGE_UID,
]


MAX_UID_LENGTH = 64
AVAILABLE_UID_DIGETS = MAX_UID_LENGTH - len(_RAI_CLIENT_ROOT_UID_PREFIX)


@functools.lru_cache()
def machine_uid():
    return generate_uid(postfix=uuid.getnode())


# Built with inspiration from https://github.com/pydicom/pydicom/blob/699c9f0a8e190d463dd828822106250523d38154/pydicom/uid.py#L382-L451
# Included here so as to have guarantees from the new secrets library, a
# library which didn't exist at the time of the original implementation.
# As well as being able to customise the postfix, and have a well
# defined way to utilise the RAi prefix without directly utilising it.
def generate_uid(postfix: Optional[Union[int, str]] = None):
    if postfix is None:
        postfix_bytes = secrets.token_bytes(AVAILABLE_UID_DIGETS // 2)
        postfix = str(int.from_bytes(postfix_bytes, "big", signed=False))

    postfix = str(postfix)

    if len(postfix) > AVAILABLE_UID_DIGETS:
        postfix = postfix[:AVAILABLE_UID_DIGETS]

    uid = f"{_RAI_CLIENT_ROOT_UID_PREFIX}{postfix}"
    assert len(uid) <= MAX_UID_LENGTH
    assert re.match(pydicom.uid.RE_VALID_UID, uid)

    return uid
