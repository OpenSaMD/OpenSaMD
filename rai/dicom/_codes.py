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

from raicontours import TG263

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


DEFAULT_FMA_CODES = {
    TG263.Bone_Mandible: 52748,
    TG263.Brain: 50801,
    TG263.Brainstem: 79876,
    TG263.Cochlea_L: 60203,
    TG263.Cochlea_R: 60202,
    TG263.Glnd_Lacrimal_L: 59103,
    TG263.Glnd_Lacrimal_R: 59102,
    TG263.Lens_L: 58243,
    TG263.Lens_R: 58242,
    TG263.Lung_L: 7310,
    TG263.Lung_R: 7309,
    TG263.OpticChiasm: 62045,
    TG263.OpticNrv_L: 50878,
    TG263.OpticNrv_R: 50875,
    TG263.Eye_L: 12515,
    TG263.Eye_R: 12514,
    TG263.Parotid_L: 59798,
    TG263.Parotid_R: 59797,
    TG263.SpinalCanal: 9680,
    TG263.SpinalCord: 7647,
    TG263.Glnd_Submand_L: 59803,
    TG263.Glnd_Submand_R: 59802,
}


FMA_NAMES = {
    7196: "Spleen",
    13889: "Pituitary gland",
    7198: "Pancreas",
    3862: "Anterior interventricular branch of left coronary artery",
    5906: "Brachial nerve plexus",
    7088: "Heart",
    7131: "Esophagus",
    7148: "Stomach",
    7197: "Liver",
    7200: "Small intestine",
    7201: "Large intestine",
    7202: "Gallbladder",
    7204: "Right kidney",
    7205: "Left kidney",
    7206: "Duodenum",
    7309: "Right lung",
    7310: "Left lung",
    7394: "Trachea",
    7465: "Carina of trachea",
    7486: "Manubrium",
    7647: "Spinal cord",
    9600: "Prostate",
    9680: "Vertebral canal",
    12514: "Right eyeball",
    12515: "Left eyeball",
    14544: "Rectum",
    15900: "Urinary bladder",
    16580: "Bony pelvis",
    19386: "Seminal vesicle",
    20292: "Cavity of mouth",
    45244: "Right brachial nerve plexus",
    45245: "Left brachial nerve plexus",
    45643: "External genitalia",
    50060: "Chest wall",
    50801: "Brain",
    50875: "Right optic nerve",
    50878: "Left optic nerve",
    52590: "Cauda equina",
    52748: "Mandible",
    54640: "Tongue",
    54832: "Temporomandibular joint",
    54833: "Right temporomandibular joint",
    54834: "Left temporomandibular joint",
    54966: "Set of constrictor muscles of pharynx",
    55011: "Head of right femur",
    55012: "Head of left femur",
    55097: "Larynx",
    55414: "Glottis",
    58242: "Right lens",
    58243: "Left lens",
    59102: "Right lacrimal gland",
    59103: "Left lacrimal gland",
    59797: "Right parotid gland",
    59798: "Left parotid gland",
    59802: "Right submandibular gland",
    59803: "Left submandibular gland",
    60202: "Right cochlea",
    60203: "Left cochlea",
    61825: "Temporal lobe",
    62045: "Optic chiasm",
    67944: "Cerebellum",
    71331: "Set of ribs",
    79876: "Brainstem",
    223695: "Left nipple",
    235068: "Parasternal lymphatic chain",
    256135: "Body",
    275022: "Right hippocampus",
    275024: "Left hippocampus",
}
