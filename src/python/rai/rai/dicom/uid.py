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

import pydicom.uid

from rai._version import __version__

# Many thanks to the Medical Connections for offering free
# valid UIDs (http://www.medicalconnections.co.uk/FreeUID.html)
# Their service was used to obtain the following root UID for
# Radiotherapy AI:
_RAI_ROOT_UID_PREFIX = "1.2.826.0.1.3680043.10.756."

_RAI_INTERNAL_ROOT_UID_PREFIX = f"{_RAI_ROOT_UID_PREFIX}0."

_RAI_CONTOURS_PRODUCT_ID = "1"

RAI_CLIENT_ROOT_UID_PREFIX = f"{_RAI_ROOT_UID_PREFIX}1."
RAI_IMPLEMENTATION_VERSION_NAME = f"rai-v{__version__}"

RAI_CONTOURS_IMPLEMENTATION_CLASS_UID = (
    f"{_RAI_INTERNAL_ROOT_UID_PREFIX}{_RAI_CONTOURS_PRODUCT_ID}.{__version__}"
)
assert re.match(pydicom.uid.RE_VALID_UID, RAI_CONTOURS_IMPLEMENTATION_CLASS_UID)
