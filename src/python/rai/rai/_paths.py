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

import os
import pathlib

HOME = pathlib.Path.home()
RAI_HOME_DIR = pathlib.Path.home() / ".rai"
RAI_DATA = RAI_HOME_DIR / "data"

# TODO: Need a robust way to get the repo directory when using pants

if os.getenv("CI"):
    REPO_ROOT = pathlib.Path("/home/runner/work/OpenSaMD/OpenSaMD")
else:
    REPO_ROOT = HOME / "git" / "OpenSaMD"

DOCS_DIR = REPO_ROOT / "docs"
PYTHON_PACKAGES_DIR = REPO_ROOT / "src" / "python"

RAI_DIR = PYTHON_PACKAGES_DIR / "rai"
RAICONTOURS_DIR = PYTHON_PACKAGES_DIR / "raicontours"

TEST_RECORDS_DIR = REPO_ROOT / "records" / "tests" / "python"
