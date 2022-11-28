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


# https://github.com/RadiotherapyAI/FMA/raw/367d57c04521f1c50f633b82d9827ee025cf5402/FMA.csv

import pathlib
import urllib.request

HERE = pathlib.Path(__file__).parent


def download_prune_and_create_fma_descriptions_json():
    url = "https://github.com/RadiotherapyAI/FMA/raw/367d57c04521f1c50f633b82d9827ee025cf5402/FMA.csv"

    # TODO: Automate the creation of the description dictionary
