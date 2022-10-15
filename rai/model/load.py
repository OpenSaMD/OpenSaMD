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

import raicontours

from . import _create

Config = raicontours.Config


def load_model(cfg: Config):
    starting_model, dependent_model = _create.create_model(cfg)

    # Only need to load the weights for one model, as both models share
    # the same weights internally.
    starting_model.load_weights(cfg["model_path"])

    return starting_model, dependent_model
