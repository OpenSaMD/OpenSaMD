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

"""Model creation record utilities"""


import json
from functools import lru_cache
from typing import Set, Tuple

import pydicom

from raicontours._paths import HERE
from raicontours.typing import UtilisationRecord


def dicom_utilisation(ds: pydicom.Dataset):
    """Determine the utilisation status of a given pydicom dataset"""

    training, validation = _training_record()

    study_uid = ds.StudyInstanceUID

    if study_uid in training:
        return UtilisationRecord.TRAINING

    if study_uid in validation:
        return UtilisationRecord.VALIDATION

    return UtilisationRecord.NOT_USED


@lru_cache(maxsize=None)
def _training_record() -> Tuple[Set[str], Set[str]]:
    with open(HERE / "training_record.json", encoding="utf8") as f:
        data = json.load(f)

    training: Set[str] = set(data["training"])
    validation: Set[str] = set(data["validation"])

    return training, validation
