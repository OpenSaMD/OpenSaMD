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

"""Module for propagating dependent data throughout the repository"""

import pathlib
import re
import textwrap
from typing import Dict, cast

import black
import tomlkit
from typing_extensions import Literal

from rai._paths import RAICONTOURS_REPO_ROOT, REPO_ROOT

PyProjectContents = Dict[
    Literal["tool"], Dict[Literal["poetry"], Dict[Literal["version"], str]]
]

AUTOGEN_MESSAGE = [
    "# DO NOT EDIT THIS FILE!",
    "# This file has been autogenerated by `rai propagate`",
]


def run():
    """Undergo data propagation."""
    _propagate_python_version(REPO_ROOT)
    _propagate_product_version(REPO_ROOT, update_docs=True)
    _propagate_product_version(RAICONTOURS_REPO_ROOT, update_docs=False)


def _propagate_python_version(repo_root: pathlib.Path):
    python_version = _get_python_version()

    docs_dir = _get_docs_dir(repo_root)

    _update_ci(repo_root, python_version)
    _update_docs_python_version(docs_dir, python_version)


def _get_docs_dir(repo_root: pathlib.Path):
    docs_dir = repo_root / "docs"
    return docs_dir


def _propagate_product_version(repo_root: pathlib.Path, update_docs: bool):
    device_version = _get_device_version(repo_root)

    repo_name = repo_root.name
    library_dir = repo_root / repo_name

    _update_library_version_file(library_dir, device_version)

    if update_docs:
        docs_dir = _get_docs_dir(repo_root)
        _update_docs_device_version(docs_dir, device_version)


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


def _get_device_version(repo_root: pathlib.Path):
    pyproject_path = repo_root / "pyproject.toml"

    with open(pyproject_path, encoding="utf8") as f:
        pyproject_contents = tomlkit.loads(f.read())

    pyproject_contents = cast(PyProjectContents, pyproject_contents)

    product_version = pyproject_contents["tool"]["poetry"]["version"]

    return product_version


def _update_ci(repo_root: pathlib.Path, python_version: str):
    _replace_key_in_yaml_file(
        path=repo_root / ".github" / "workflows" / "main.yml",
        key="python-version",
        new_value=f'"{python_version}"',
    )


def _update_docs_python_version(docs_dir: pathlib.Path, python_version: str):
    _replace_key_in_yaml_file(
        path=docs_dir / "_config.yml",
        key="python_version",
        new_value=f'"{python_version}"',
    )


def _update_library_version_file(library_dir: pathlib.Path, device_version: str):
    device_version_list = re.split(r"[-\.]", device_version)

    for i, item in enumerate(device_version_list):
        try:
            device_version_list[i] = int(item)
        except ValueError:
            pass

    version_contents = textwrap.dedent(
        f"""\
            {AUTOGEN_MESSAGE[0]}
            {AUTOGEN_MESSAGE[1]}

            \"""Package version information\"""

            version_info = {device_version_list}
            __version__ = "{device_version}"
        """
    )

    version_contents = black.format_str(version_contents, mode=black.FileMode())
    version_file_path = library_dir / "_version.py"

    with open(version_file_path, "w", encoding="utf8") as f:
        f.write(version_contents)


def _update_docs_device_version(docs_dir: pathlib.Path, device_version: str):
    _replace_key_in_yaml_file(
        path=docs_dir / "_config.yml",
        key="device_version",
        new_value=f'"`v{device_version}`"',
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