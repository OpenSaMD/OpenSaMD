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
import subprocess

from ._paths import DOCS_DIR, REPO_ROOT


def build(clean: bool):
    """Build the Jupyter Book documentation"""

    env = os.environ.copy()

    if clean:
        subprocess.check_call(
            ["jupyter-book", "clean", str(DOCS_DIR)], cwd=REPO_ROOT, env=env
        )

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
