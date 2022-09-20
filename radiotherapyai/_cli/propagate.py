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

"""Module for propagating dependent data throughout the repository"""

import pathlib
import re

from ._paths import DOCS_DIR, REPO_ROOT


def run():
    """Undergo data propagation."""
    _propagate_python_version()


def _propagate_python_version():
    python_version = _get_python_version()

    _update_ci(python_version)
    _update_docs_macros(python_version)


def _get_python_version():
    python_version = None

    tool_versions_path = REPO_ROOT / ".tool-versions"

    with open(tool_versions_path, "r", encoding="utf8") as f:
        for line in f:
            line_items = line.split(" ")
            if line_items[0] == "python":
                python_version = line_items[1].strip()
                break

    if python_version is None:
        raise ValueError(f"No Python version found within {tool_versions_path}")

    return python_version


def _update_ci(python_version: str):
    _replace_key_in_yaml_file(
        path=REPO_ROOT / ".github" / "workflows" / "main.yml",
        key="python-version",
        new_value=f'"{python_version}"',
    )


def _update_docs_macros(python_version: str):
    _replace_key_in_yaml_file(
        path=DOCS_DIR / "_config.yml",
        key="python_version",
        new_value=f'"{python_version}"',
    )


def _replace_key_in_yaml_file(path: pathlib.Path, key: str, new_value: str):
    with open(path, "r", encoding="utf8") as f:
        lines = f.readlines()

    pattern = re.compile(rf"(^ *){key}: .*$")
    for i, line in enumerate(lines):
        match = re.match(pattern, line)
        if match is None:
            continue

        spaces = match.group(1)
        new_line = f"{spaces}{key}: {new_value}\n"

        lines[i] = new_line

    with open(path, "w", encoding="utf8") as f:
        f.writelines(lines)
