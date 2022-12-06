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

# pylint: disable = invalid-name, useless-import-alias

from __future__ import annotations

import json
import pathlib
from enum import Enum
from functools import lru_cache
from typing import Set, Tuple, Union

import pydicom
from typing_extensions import TypedDict

from ._version import __version__ as __version__
from ._version import version_info as version_info
from .tg263 import TG263 as TG263

_HERE = pathlib.Path(__file__).parent.resolve()
_model_path = _HERE / "model.h5"


StructureName = Union[str, TG263]


class UtilisationRecord(str, Enum):
    Training = "training"
    Validation = "validation"
    NotUsed = "not-used"


def dicom_utilisation(ds: pydicom.Dataset):
    training, validation = _training_record()

    study_uid = ds.StudyInstanceUID

    if study_uid in training:
        return UtilisationRecord.Training

    if study_uid in validation:
        return UtilisationRecord.Validation

    return UtilisationRecord.NotUsed


@lru_cache(maxsize=None)
def _training_record() -> Tuple[Set[str], Set[str]]:
    with open(_HERE / "training_record.json", encoding="utf8") as f:
        data = json.load(f)

    training: Set[str] = set(data["training"])
    validation: Set[str] = set(data["validation"])

    return training, validation


class ContourOptions(TypedDict, total=False):
    from_mask: TG263
    mask_level: float
    union: list[StructureName]
    difference: list[StructureName]
    intersection: list[StructureName]
    # buffer: float
    colour: str
    display: bool


class Config(TypedDict):
    """The model configuration"""

    model_path: pathlib.Path
    structures: list[StructureName]
    patch_dimensions: tuple[int, int, int]
    encoding_filter_counts: list[int]
    decoding_filter_counts: list[int]
    rescale_slope: float
    rescale_intercept: float
    reduce_block_sizes: list[tuple[int, int, int]]
    reduce_algorithms: list[str]
    mask_level: float
    mask_level_overrides: dict[StructureName, float]
    # contours: dict[StructureName, ContourOptions]


def get_config():
    # By (re)creating cfg within a function, separate cfg instances are
    # protected from mutating each other.
    cfg: Config = {
        "model_path": _model_path,
        # "structures": [
        #     TG263.Heart,
        #     TG263.Liver,
        # ],
        "structures": [
            TG263.Eye_L,
            TG263.Eye_R,
            TG263.Glnd_Lacrimal_L,
            TG263.Glnd_Lacrimal_R,
            TG263.Lens_L,
            TG263.Lens_R,
            TG263.OpticChiasm,
            TG263.OpticNrv_L,
            TG263.OpticNrv_R,
        ],
        # "structures": [
        #     TG263.Bladder,
        #     TG263.Bone_Mandible,
        #     TG263.Brain,
        #     TG263.Brainstem,
        #     TG263.Carina,
        #     TG263.Cavity_Oral,
        #     TG263.Cochlea_L,
        #     TG263.Cochlea_R,
        #     TG263.Duodenum,
        #     TG263.Esophagus,
        #     TG263.Eye_L,
        #     TG263.Eye_R,
        #     TG263.Glnd_Adrenal_L,
        #     TG263.Glnd_Adrenal_R,
        #     TG263.Glnd_Lacrimal_L,
        #     TG263.Glnd_Lacrimal_R,
        #     TG263.Glnd_Submand_L,
        #     TG263.Glnd_Submand_R,
        #     TG263.Heart,
        #     TG263.Kidney_L,
        #     TG263.Kidney_R,
        #     TG263.Larynx,
        #     TG263.Lens_L,
        #     TG263.Lens_R,
        #     TG263.Liver,
        #     TG263.Lung_L,
        #     TG263.Lung_R,
        #     TG263.Musc_Constrict,
        #     TG263.OpticChiasm,
        #     TG263.OpticNrv_L,
        #     TG263.OpticNrv_R,
        #     TG263.Pancreas,
        #     TG263.Parotid_L,
        #     TG263.Parotid_R,
        #     TG263.Rectum,
        #     TG263.SpinalCanal,
        #     TG263.SpinalCord,
        #     TG263.Spleen,
        #     TG263.Stomach,
        #     TG263.Trachea,
        # ],
        "patch_dimensions": (64, 64, 64),
        "encoding_filter_counts": [32, 64, 128, 256],
        "decoding_filter_counts": [128, 64, 32, 16],
        "rescale_slope": 4000.0,
        "rescale_intercept": -1024.0,
        "reduce_block_sizes": [(2, 4, 4), (1, 2, 2), (1, 1, 1)],
        "reduce_algorithms": ["min", "mean", "median", "max"],
        "mask_level": 127.5,
        "mask_level_overrides": {
            # TG263.Lens_L: 50,
            # TG263.Lens_R: 50,
            # TG263.OpticChiasm: 50,
            # TG263.OpticNrv_L: 50,
            # TG263.OpticNrv_R: 50,
            # TG263.Eye_L: 100,
            # TG263.Eye_R: 100,
            # TG263.Glnd_Lacrimal_L: 50,
            # TG263.Glnd_Lacrimal_R: 50,
            # TG263.Glnd_Submand_L: 100,
            # TG263.Glnd_Submand_R: 100,
            # TG263.Musc_Constrict: 1.5,
            # TG263.Trachea: 80,
            # TG263.Esophagus: 80,
            # TG263.Cochlea_L: 50,
            # TG263.Cochlea_R: 50,
            # TG263.Larynx: 50,
            # TG263.Parotid_L: 70,
            # TG263.Parotid_R: 70,
            # TG263.Bone_Mandible: 110,
            # TG263.Cavity_Oral: 80,
            # TG263.Brainstem: 127.5,
        },
    }

    return cfg


def get_mask_level(cfg: Config, structure_name: StructureName):
    try:
        mask_level = cfg["mask_level_overrides"][structure_name]
    except KeyError:
        mask_level = cfg["mask_level"]

    return mask_level


# TODO: Add a "uids used for training" list and use it to verify a DICOM
# file can be used for metric calculation.


# "contours": {
#     TG263.Lens_L: {
#         "from_mask": TG263.Lens_L,
#         "mask_level": 50,
#         "colour": "aqua blue",
#     },
#     TG263.Lens_R: {
#         "from_mask": TG263.Lens_R,
#         "mask_level": 50,
#         "colour": "aqua green",
#     },
#     TG263.OpticNrv_L: {
#         "from_mask": TG263.OpticNrv_L,
#         "mask_level": 127.5,
#         "colour": "deep red",
#     },
#     TG263.OpticNrv_R: {
#         "from_mask": TG263.OpticNrv_R,
#         "mask_level": 127.5,
#         "colour": "orange red",
#     },
#     f"{TG263.OpticNrv_L.value} Generous": {
#         "from_mask": TG263.OpticNrv_L,
#         "mask_level": 50,
#         "colour": "#2c6fbb",
#     },
#     f"{TG263.OpticNrv_R.value} Generous": {
#         "from_mask": TG263.OpticNrv_R,
#         "mask_level": 50,
#         "colour": "#39ad48",
#     },
#     TG263.Eye_L: {"from_mask": TG263.Eye_L, "mask_level": 100},
#     TG263.Eye_R: {"from_mask": TG263.Eye_R, "mask_level": 100},
#     TG263.Glnd_Lacrimal_L: {
#         "from_mask": TG263.Glnd_Lacrimal_L,
#         "mask_level": 100,
#     },
#     TG263.Glnd_Lacrimal_R: {
#         "from_mask": TG263.Glnd_Lacrimal_R,
#         "mask_level": 100,
#     },
#     TG263.Eyes: {
#         "union": [TG263.Eye_L, TG263.Eye_R],
#     },
#     # "Eyes + 3mm": {
#     #     "union": [TG263.Eyes],
#     #     "buffer": 3,
#     # },
#     # "Eyes - 3mm": {
#     #     "union": [TG263.Eyes],
#     #     "buffer": -3,
#     # },
#     # TG263.Lens: {
#     #     "union": [TG263.Lens_L, TG263.Lens_R],
#     #     "display": False,
#     # },
#     # "Lens + 3mm": {
#     #     "union": [TG263.Lens],
#     #     "buffer": 3,
#     # },
#     "Eyes - Lens": {
#         "union": [TG263.Eyes],
#         "difference": [TG263.Lens_L, TG263.Lens_R],
#         "display": False,
#     },
