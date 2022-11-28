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


import enum
import functools
import re
from typing import NamedTuple

import pydicom
import pydicom.datadict

from rai.vendor.innolitics.standard.load import get_standard


class AttributeType(enum.Enum):
    """DICOM Data Element attribute requirement types.

    See <https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_7.4.html>
    """

    REQUIRED = "1"
    CONDITIONALLY_REQUIRED = "1C"
    REQUIRED_EMPTY_IF_UNKNOWN = "2"
    CONDITIONALLY_REQUIRED_EMPTY_IF_UNKNOWN = "2C"
    OPTIONAL = "3"


class Usage(str, enum.Enum):
    """DICOM module usage requirements

    See the usage column within
    <https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.19.3.html#table_A.19.3-1>
    """

    MANDATORY = "M"
    USER_OPTIONAL = "U"


class Inheritance(str, enum.Enum):
    """Whether or not a given module should be inherited from the
    original CT series, or if it should be created fresh within the
    new RT Structure file.
    """

    CREATE = "create"
    INHERIT = "inherit"


class ModuleOptions(NamedTuple):
    """The options for a given module.

    Used to represent the following table:
    https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.19.3.html#table_A.19.3-1
    """

    usage: Usage
    inheritance: Inheritance


# Encoding of the RT Structure Set IOD Modules table. Original table
# available at:
# <https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.19.3.html#table_A.19.3-1>
RTSTRUCT_DICOM_MODULES = {
    # IE Patient
    "patient": ModuleOptions(Usage.MANDATORY, Inheritance.INHERIT),
    "clinical-trial-subject": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    # IE Study
    "general-study": ModuleOptions(Usage.MANDATORY, Inheritance.INHERIT),
    "patient-study": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    "clinical-trial-study": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    # IE Series
    "rt-series": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "clinical-trial-series": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
    # IE Equipment
    "general-equipment": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    # IE Frame of Reference
    "frame-of-reference": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    # IE Structure Set
    "structure-set": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "roi-contour": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "rt-roi-observations": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "approval": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
    "general-reference": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
    "sop-common": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "common-instance-reference": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
}


@functools.lru_cache()
def get_keyword_types_for_module(module_id):
    keyword_types = {
        _string_tag_to_dicom_keyword(item["tag"]): AttributeType(item["type"])
        for item in get_standard("module_to_attributes")
        if item["moduleId"] == module_id and len(item["path"].split(":")) == 2
    }

    return keyword_types


def _string_tag_to_dicom_keyword(tag):
    tag = tag.replace(" ", "")
    match = re.match(r"\(([0-9A-F]+),([0-9A-F]+)\)", tag)

    if match is None:
        raise ValueError(f"The tag {tag} was unable to be converted to a DICOM keyword")

    groups = match.groups()
    tag = (int(groups[0], 16), int(groups[1], 16))
    keyword = pydicom.datadict.keyword_for_tag(tag)

    return keyword
