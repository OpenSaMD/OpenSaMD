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

"""Helper script to build the jupyter-book with pants"""

import pathlib

import jupyter_book.cli.main
import yaml
from sphinx_external_toc.parsing import create_toc_dict
from sphinx_external_toc.tools import create_site_map_from_path

# TODO: Need a robust way to get the repo directory when using pants
REPO_ROOT = pathlib.Path("/home/runner/work/OpenSaMD/OpenSaMD")

if not REPO_ROOT.exists():
    REPO_ROOT = pathlib.Path.home() / "git" / "OpenSaMD"


DOCS_DIR = REPO_ROOT / "docs"


def _main():
    site_map = create_site_map_from_path(DOCS_DIR)
    data = create_toc_dict(site_map)

    with open(DOCS_DIR / "_toc.yml", "w", encoding="utf8") as f:
        f.write(yaml.dump(data, sort_keys=False, default_flow_style=False))

    jupyter_book.cli.main.build(  # pylint: disable = no-value-for-parameter
        [str(DOCS_DIR)]
    )


if __name__ == "__main__":
    _main()
