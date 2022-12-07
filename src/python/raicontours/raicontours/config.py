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


"""RAi contours model configuration"""

import pathlib
from typing import Union

from typing_extensions import TypedDict

from raicontours._paths import model_path
from raicontours.typing import TG263

StructureName = Union[str, TG263]


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


def get_config():
    """Get the raicontours configuration"""

    # By (re)creating cfg within a function, separate cfg instances are
    # protected from mutating each other.
    cfg: Config = {
        "model_path": model_path,
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
        "mask_level_overrides": {},
    }

    return cfg


def get_mask_level(cfg: Config, structure_name: StructureName):
    """Determine the configuration mask level for a given structure.

    This defaults to cfg['mask_level'] while taking into account the
    individual structure overrides within cfg['mask_level_overrides'].
    """

    try:
        mask_level = cfg["mask_level_overrides"][structure_name]
    except KeyError:
        mask_level = cfg["mask_level"]

    return mask_level
