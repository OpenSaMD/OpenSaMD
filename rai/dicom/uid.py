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

"""DICOM UID constants and tools"""

import re
import secrets
from typing import Optional, Union

import pydicom.uid

from rai._version import __version__

# Many thanks to the Medical Connections for offering free
# valid UIDs (http://www.medicalconnections.co.uk/FreeUID.html)
# Their service was used to obtain the following root UID for
# Radiotherapy AI:
RAI_ROOT_UID = "1.2.826.0.1.3680043.10.756."

RAI_INTERNAL_ROOT_UID = f"{RAI_ROOT_UID}0."
RAI_CLIENT_ROOT_UID = f"{RAI_ROOT_UID}1."

PRODUCT_ID = "000000"

RAI_IMPLEMENTATION_CLASS_UID = f"{RAI_INTERNAL_ROOT_UID}{PRODUCT_ID}.{__version__}"
RAI_IMPLEMENTATION_VERSION_NAME = f"rai-v{__version__}"

MAX_UID_LENGTH = 64
AVAILABLE_UID_DIGITS = MAX_UID_LENGTH - len(RAI_CLIENT_ROOT_UID)

# Built with inspiration from:
# https://github.com/pydicom/pydicom/blob/699c9f0a8/pydicom/uid.py#L382-L451
def generate_uid(postfix: Optional[Union[int, str]] = None):
    """Generate an RAI DICOM UID"""

    if postfix is None:
        postfix_bytes = secrets.token_bytes(AVAILABLE_UID_DIGITS // 2)
        postfix = int.from_bytes(postfix_bytes, "big", signed=False)

    postfix = str(postfix)

    if len(postfix) > AVAILABLE_UID_DIGITS:
        postfix = postfix[:AVAILABLE_UID_DIGITS]

    uid = f"{RAI_CLIENT_ROOT_UID}{postfix}"
    assert len(uid) <= MAX_UID_LENGTH
    assert re.match(pydicom.uid.RE_VALID_UID, uid)

    return uid
