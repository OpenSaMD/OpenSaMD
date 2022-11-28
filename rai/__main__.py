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

# pylint: disable = import-outside-toplevel

"""CLI entrance

Currently only utilised to build the docs
"""

import click


@click.group()
def cli():
    """The Radiotherapy AI command line interface"""


@cli.command()
@click.option("--clean/--no-clean", default=False)
def docs(clean: bool):
    """Build the Radiotherapy AI regulatory documentation"""
    from ._cli import docs as _docs

    _docs.build(clean)


@cli.command()
def propagate():
    """Propagate various dependent items throughout the repository

    For example, version numbers.
    """
    from ._cli import propagate as _propagate

    _propagate.run()


@cli.command()
def prune():
    from rai.vendor.innolitics.standard import prune as _prune

    _prune.prune_module_attributes()


if __name__ == "__main__":
    cli()
