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

"""Repository paths utilised by the CLI module"""

import pathlib

HERE = pathlib.Path(__file__)
REPO_ROOT = pathlib.Path(HERE.parents[1])
DOCS_DIR = REPO_ROOT / "docs"
LIBRARY_DIR = REPO_ROOT / "rai"

RAI_HOME_DIR = pathlib.Path.home() / ".rai"
RAI_DATA = RAI_HOME_DIR / "data"

GIT_DIR = REPO_ROOT.parent
RAICONTOURS_REPO_ROOT = GIT_DIR / "raicontours"
RAICONTOURS_LIBRARY_DIR = RAICONTOURS_REPO_ROOT / "raicontours"
