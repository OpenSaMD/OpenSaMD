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


import ast


def parse_imports(filepath):
    """Formulate a dictionary of imports within a python file for usage by ``apipkg``.

    Parameters
    ----------
    filepath
        The python file containing the imports to be parsed.

    Returns
    -------
    imports_for_apipkg
        A dictionary of imports in the format expected by ``apipkg``.

    """
    with open(filepath) as f:
        imports_string = f.read()

    imports_for_apipkg = {}

    for node in ast.parse(imports_string).body:
        if not isinstance(node, ast.Import):
            raise ValueError("Only direct import statements are supported")

        aliases = list(node.names)
        if len(aliases) != 1:
            raise ValueError("Only one alias per import supported")

        alias = aliases[0]
        asname = alias.asname

        if asname is None:
            asname = alias.name

        imports_for_apipkg[asname] = alias.name

    return imports_for_apipkg
