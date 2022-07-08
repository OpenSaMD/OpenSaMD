# Copyright (C) 2022 Radiotherapy AI Pty Ltd

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

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

    subprocess.check_call(
        ["jupyter-book", "build", str(DOCS_DIR)], cwd=REPO_ROOT, env=env
    )
