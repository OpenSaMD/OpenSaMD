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
from typing import NamedTuple


class AttributeType(enum.Enum):
    REQUIRED = "1"
    CONDITIONALLY_REQUIRED = "1C"
    REQUIRED_EMPTY_IF_UNKNOWN = "2"
    CONDITIONALLY_REQUIRED_EMPTY_IF_UNKNOWN = "2C"
    OPTIONAL = "3"


class Usage(str, enum.Enum):
    MANDATORY = "M"
    USER_OPTIONAL = "U"


class Inheritance(str, enum.Enum):
    CREATE = "create"
    INHERIT = "inherit"


class ModuleOptions(NamedTuple):
    usage: Usage
    inheritance: Inheritance


RTSTRUCT_DICOM_MODULES = {
    "patient": ModuleOptions(Usage.MANDATORY, Inheritance.INHERIT),
    "general-study": ModuleOptions(Usage.MANDATORY, Inheritance.INHERIT),
    "patient-study": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    "rt-series": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "clinical-trial-subject": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    "clinical-trial-study": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    "clinical-trial-series": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
    "general-equipment": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "frame-of-reference": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.INHERIT),
    "structure-set": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "roi-contour": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "rt-roi-observations": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "approval": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
    "general-reference": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
    "sop-common": ModuleOptions(Usage.MANDATORY, Inheritance.CREATE),
    "common-instance-reference": ModuleOptions(Usage.USER_OPTIONAL, Inheritance.CREATE),
}
