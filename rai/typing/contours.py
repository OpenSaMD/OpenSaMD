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

from typing import Dict, List, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from typing_extensions import Literal

from raicontours import TG263

Grid = NDArray[np.float64]
Mask = NDArray[np.uint8]

# TODO: Differentiate these with NDArray shape parameters when that's
# available
MaskStack = Mask
AllStructuresMaskStack = MaskStack


ContourXY = List[Tuple[float, float]]
ContoursXY = List[ContourXY]

ContoursBySlice = List[ContoursXY]

StructureName = Union[str, TG263]
ContoursByStructure = Dict[StructureName, ContoursBySlice]

Orienation = Literal["transverse", "coronal", "sagittal"]
ContoursByOrientation = Dict[Orienation, ContoursByStructure]
