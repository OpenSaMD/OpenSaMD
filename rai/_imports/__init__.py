# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
# Copyright (C) 2020 Simon Biggs

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

import importlib
import pathlib

from rai._imports import _parse
from rai.vendor import apipkg

HERE = pathlib.Path(__file__).parent

imports_for_apipkg = _parse.parse_imports(HERE.joinpath("imports.py"))
apipkg.initpkg(__name__, imports_for_apipkg)  # type: ignore

THIS = importlib.import_module(__name__)
IMPORTABLES = dir(THIS)

# This will never actually run, but it helps pylint know what's going on
if "numpy" not in IMPORTABLES:
    print(IMPORTABLES)

    from .imports import *

    raise ValueError("This section of code should never run")
