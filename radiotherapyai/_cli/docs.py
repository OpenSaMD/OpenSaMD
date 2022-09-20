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

"""Building the documentation"""

import os
import pathlib
import subprocess

HERE = pathlib.Path(__file__)
REPO_ROOT = HERE.parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SRC_DIR = REPO_ROOT / "src"
TABLE_OF_CONTENTS_PATH = DOCS_DIR / "_toc.yml"


def build():
    """Build the Jupyter Book documentation"""

    env = os.environ.copy()

    with open(DOCS_DIR / "_toc.yml", "w", encoding="utf8") as f:
        subprocess.check_call(
            ["jupyter-book", "toc", "from-project", str(DOCS_DIR)],
            cwd=REPO_ROOT,
            env=env,
            stdout=f,
        )
    subprocess.check_call(
        ["jupyter-book", "build", str(DOCS_DIR)], cwd=REPO_ROOT, env=env
    )
