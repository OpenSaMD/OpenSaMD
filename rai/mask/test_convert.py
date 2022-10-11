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
from typing import TypedDict

import matplotlib.pyplot as plt  # pyright: ignore [reportMissingTypeStubs, reportUnknownVariableType]
import numpy as np

from rai.metrics import dice
from rai.typing.contours import ContoursXY, Grid

from .convert import contours_to_mask, mask_to_contours

HERE = pathlib.Path(__file__).parent
FIGURE_DIR = HERE / "test_figures"


def test_conversion_round_trip():
    """Test a round trip of contours -> mask -> contours"""

    cases: list[_TestCase] = []

    cases.append(
        {
            "title": "edge-of-mask",
            "x_grid": np.array([0, 1, 2, 3]),
            "y_grid": np.array([10, 12, 14, 16]),
            "contours": [[(-0.5, 9), (2, 9), (2, 14), (-0.5, 14)]],
            "dice_lower_bound": 0.90,
        }
    )

    t = np.linspace(0, 2 * np.pi)
    x = 1.5 * np.sin(t)
    y = np.cos(t) + 0.5

    cases.append(
        {
            "title": "offset-ellipse",
            "x_grid": np.linspace(-2, 2, 21),
            "y_grid": np.linspace(-2, 2, 31),
            "contours": [list(zip(x, y))],
            "dice_lower_bound": 0.99,
        }
    )

    cases.append(
        {
            "title": "right-angle-triangle",
            "x_grid": np.linspace(0, 4, 5),
            "y_grid": np.linspace(0, 10, 11),
            "contours": [[(0, 0), (0, 10), (2, 0), (0, 0)]],
            # TODO: This results in an overlapping contour. Contour
            # overlaps like this need to be cleaned up with shapely in
            # post-processing.
            "dice_lower_bound": 0.81,  # Sharp sub-pixel points are not handled well
        }
    )

    x_left = np.sin(t)
    y = np.cos(t)

    x_right = x_left + 2

    contours = [
        list(zip(x_left, y)),
        list(zip(x_right, y)),
    ]

    cases.append(
        {
            "title": "two-small-abutting-circles",
            "x_grid": np.linspace(-1, 4, 13),
            "y_grid": np.linspace(-2, 2, 6),
            "contours": contours,
            "dice_lower_bound": 0.94,
        }
    )

    for case in cases:
        _run_round_trip_test(**case)


class _TestCase(TypedDict):
    title: str
    x_grid: Grid
    y_grid: Grid
    contours: ContoursXY
    dice_lower_bound: float


def _run_round_trip_test(
    title: str,
    x_grid: Grid,
    y_grid: Grid,
    contours: ContoursXY,
    dice_lower_bound: float,
):
    mask = contours_to_mask(x_grid, y_grid, contours)
    round_trip_contours = mask_to_contours(x_grid, y_grid, mask)

    assert dice.from_contours(a=contours, b=round_trip_contours) >= dice_lower_bound

    (
        fig,  # pyright: ignore [reportUnknownVariableType]
        ax,  # pyright: ignore [reportUnknownVariableType]
    ) = plt.subplots()  # pyright: ignore [reportUnknownMemberType]
    c = ax.pcolormesh(  # pyright: ignore [reportUnknownMemberType, reportUnknownVariableType]
        x_grid, y_grid, mask, shading="nearest"
    )
    fig.colorbar(c)  # pyright: ignore [reportUnknownMemberType]

    for contour in contours:
        contour_array = np.array(contour)
        ax.plot(  # pyright: ignore [reportUnknownMemberType]
            contour_array[:, 0],
            contour_array[:, 1],
            "C3",
            lw=4,
            label="original contour",
        )

    for contour in round_trip_contours:
        contour_array = np.array(contour)
        ax.plot(  # pyright: ignore [reportUnknownMemberType]
            contour_array[:, 0],
            contour_array[:, 1],
            "k--",
            lw=2,
            label="round-trip contour",
        )

    ax.set_aspect("equal")  # pyright: ignore [reportUnknownMemberType]
    ax.set_title(title)  # pyright: ignore [reportUnknownMemberType]
    fig.legend(loc="upper left")  # pyright: ignore [reportUnknownMemberType]

    fig.savefig(FIGURE_DIR / f"{title}.png")  # type: ignore


# For this test to pass, need to implement contour keyhole technique.
# https://dicom.nema.org/medical/Dicom/2022b/output/chtml/part03/sect_C.8.8.6.3.html
# I'll include that in a follow up PR, given this PR is getting large
# already.
def test_round_trip_with_nested_contours():
    """Test round trip with nested contours"""
