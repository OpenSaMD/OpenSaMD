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


"""Testing the mask conversion to and from contour lines"""

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from radiotherapyai.metrics import dice

from .convert import contours_to_mask, mask_to_contours

HERE = pathlib.Path(__file__).parent
FIGURE_DIR = HERE / "test_figures"


def test_mask_at_edge_of_image():
    """Test the effect of a contour at the edge of an image"""
    mask = np.array(
        [
            [255, 255, 127, 0],
            [255, 255, 127, 0],
            [127, 127, 64, 0],
            [0, 0, 0, 0],
        ],
        dtype=np.uint8,
    )

    y_grid = np.array([10, 12, 14, 16])
    x_grid = np.array([0, 1, 2, 3])

    ideal_expected_contour = np.array([(9, -0.5), (9, 2), (14, 2), (14, -0.5)])
    ideal_contours = [ideal_expected_contour]

    # Marching squares doesn't perfectly follow the in-out proportion,
    # instead, it cuts off corners.
    marching_squares_expected_contour = np.array(
        [(9, 0), (10, -0.5), (12, -0.5), (14, 0), (14, 1), (12, 2), (10, 2), (9, 1)]
    )
    marching_squares_expected_contours = [marching_squares_expected_contour]

    contours = mask_to_contours(x_grid, y_grid, mask)

    assert dice.from_contours(a=contours, b=ideal_contours) > 0.89
    assert dice.from_contours(a=contours, b=marching_squares_expected_contours) > 0.99


def test_conversion_round_trip():
    """Test a round trip of contours -> mask -> contours"""

    # An offset ellipse
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

    fig, ax = plt.subplots()  # pyright: ignore [reportUnknownMemberType]
    c = ax.pcolormesh(  # pyright: ignore [reportUnknownMemberType]
        x_grid, y_grid, mask, shading="nearest"
    )
    fig.colorbar(c)  # pyright: ignore [reportUnknownMemberType]

    ax.plot(  # pyright: ignore [reportUnknownMemberType]
        x, y, "C3", lw=4, label="original contours"
    )

    for contour in round_trip_contours:
        ax.plot(  # pyright: ignore [reportUnknownMemberType]
            contour[:, 1], contour[:, 0], "--", lw=2, label="round-trip contours"
        )

    ax.set_aspect("equal")  # pyright: ignore [reportUnknownMemberType]
    fig.legend()  # pyright: ignore [reportUnknownMemberType]

    fig.savefig(FIGURE_DIR / "round-trip.png")  # type: ignore


# For this test to pass, need to implement contour keyhole technique.
# https://dicom.nema.org/medical/Dicom/2022b/output/chtml/part03/sect_C.8.8.6.3.html
# I'll include that in a follow up PR, given this PR is getting large
# already.
def test_round_trip_with_nested_contours():
    """Test round trip with nested contours"""
