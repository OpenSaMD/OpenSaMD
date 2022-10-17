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

import itertools
from typing import List, Tuple

import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np


def plot_contours_by_structure(
    x_grid, y_grid, image_stack, contours_by_structure, merge_map=None
):
    if merge_map is None:
        merge_map = {i: [key] for i, key in enumerate(contours_by_structure)}

    colour_iterator = _get_colours()

    colours = {}
    line_prop = {}
    alpha = {}
    labels = {}
    for dicom_name, tg263_names in merge_map.items():
        colour = next(colour_iterator)

        dicom_name = f"DICOM {dicom_name}"

        for name in [dicom_name] + tg263_names:
            colours[name] = colour

        line_prop[dicom_name] = "--"
        alpha[dicom_name] = 0.7

        collected_name = "DICOM"
        for name in tg263_names:
            line_prop[name] = "-"
            alpha[name] = 1
            labels[name] = f"RAi {name.value}"

            collected_name = f"{collected_name} {name.value}"

        labels[dicom_name] = collected_name

    vmin = 0.2
    vmax = 0.4

    ylim = [-np.inf, np.inf]
    xlim = [np.inf, -np.inf]

    axs = []

    for z_index in range(image_stack.shape[0]):
        has_a_contour = False

        for structure_name, contours_by_slice in contours_by_structure.items():
            contours = contours_by_slice[z_index]
            if len(contours) > 0:
                has_a_contour = True
                break

        if not has_a_contour:
            continue

        fig, ax = plt.subplots()
        axs.append(ax)

        ax.pcolormesh(
            x_grid,
            y_grid,
            image_stack[z_index, :, :],
            vmin=vmin,
            vmax=vmax,
            shading="nearest",
            cmap="gray",
        )

        for structure_name, contours_by_slice in contours_by_structure.items():
            contours = contours_by_slice[z_index]

            for contour in contours:
                contour_array = np.array(contour + [contour[0]])

                ax.plot(
                    contour_array[:, 0],
                    contour_array[:, 1],
                    line_prop[structure_name],
                    label=labels[structure_name],
                    c=colours[structure_name],
                    alpha=alpha[structure_name],
                )

                xlim[1] = np.max([np.max(contour_array[:, 0]), xlim[1]])
                xlim[0] = np.min([np.min(contour_array[:, 0]), xlim[0]])
                ylim[0] = np.max([np.max(contour_array[:, 1]), ylim[0]])
                ylim[1] = np.min([np.min(contour_array[:, 1]), ylim[1]])

        ax.set_aspect("equal", "box")

        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.title(f"Slice: {z_index}")

    x_range = xlim[1] - xlim[0]
    y_range = ylim[0] - ylim[1]

    margin = 0.2

    xlim[0] -= x_range * margin
    xlim[1] += x_range * margin

    ylim[1] -= y_range * margin
    ylim[0] += y_range * margin

    for ax in axs:
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)


def _get_colours():
    cmaps_to_pull_from = ["tab10", "Set3", "Set1", "Set2"]
    loaded_colours = []
    for cmap in cmaps_to_pull_from:
        loaded_colours += matplotlib.cm.get_cmap(cmap).colors

    colours = np.array(loaded_colours)

    greys_ref = np.logical_and(
        np.abs(colours[:, 0] - colours[:, 1]) < 0.1,
        np.abs(colours[:, 0] - colours[:, 2]) < 0.1,
        np.abs(colours[:, 1] - colours[:, 2]) < 0.1,
    )
    colours: np.ndarray = colours[np.invert(greys_ref)]
    colours: List[Tuple[float, float, float]] = [tuple(item) for item in colours]

    return itertools.cycle(colours)
