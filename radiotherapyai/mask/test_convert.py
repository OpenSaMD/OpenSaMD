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


import numpy as np

from radiotherapyai.metrics import dice

from .convert import contours_to_mask, mask_to_contours


def test_conversion_round_trip():
    """Test a round trip of contours -> mask -> contours"""

    t = np.linspace(0, 2 * np.pi, endpoint=False)
    x = 1.5 * np.sin(t)
    y = np.cos(t) + 0.5

    yx_coords = np.concatenate(  # pyright: ignore [reportUnknownMemberType]
        [y[:, None], x[:, None]], axis=-1
    )
    contours = [yx_coords]

    x_grid = np.linspace(-2, 2, 21)
    y_grid = np.linspace(-2, 2, 31)

    mask = contours_to_mask(x_grid, y_grid, contours)

    round_trip_contours = mask_to_contours(x_grid, y_grid, mask)

    assert dice.from_contours(a=contours, b=round_trip_contours) > 0.99
