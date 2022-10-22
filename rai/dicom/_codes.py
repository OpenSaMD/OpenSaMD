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

import pydicom

from . import append


def add_coding_context_and_mapping_header_items(ds: pydicom.Dataset):
    ds = append.append_dict_to_dataset(
        to_append={
            "CodingSchemeIdentificationSequence": [
                {
                    "CodingSchemeDesignator": "FMA",
                    "CodingSchemeUID": "2.16.840.1.113883.6.119",
                }
            ],
            "ContextGroupIdentificationSequence": [
                {
                    "MappingResource": "99VMS",
                    "ContextGroupVersion": "20161209",
                    "ContextIdentifier": "VMS011",
                    "ContextUID": "1.2.246.352.7.2.11",
                }
            ],
            "MappingResourceIdentificationSequence": [
                {
                    "MappingResource": "99VMS",
                    "MappingResourceUID": "1.2.246.352.7.1.1",
                    "MappingResourceName": "Varian Medical Systems",
                }
            ],
        },
        ds=ds,
    )
