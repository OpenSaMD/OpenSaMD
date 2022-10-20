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
from typing import Dict, List, Tuple

import matplotlib.animation
import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

import rai
from rai.typing.contours import ContoursByOrientation, Grid, StructureName


def view_ranges_from_masks(grids, masks):
    where_mask = np.where(masks > 127.5)
    min_mask_index = np.min(where_mask, axis=1).tolist()
    max_mask_index = np.max(where_mask, axis=1).tolist()

    slice_ranges = tuple(
        (
            list(range(min_mask_index[axis], max_mask_index[axis] + 1))
            for axis in range(3)
        )
    )

    axis_reverse = [False, True, False]
    axis_limits = tuple(
        (
            tuple(
                sorted(
                    [
                        grids[axis][min_mask_index[axis]],
                        grids[axis][max_mask_index[axis]],
                    ],
                    reverse=reverse,
                )
            )
            for axis, reverse in enumerate(axis_reverse)
        )
    )

    return slice_ranges, axis_limits


def auto_scroll_contours_by_orientation(
    grids: Tuple[Grid, Grid, Grid],
    images,
    contours_by_orientation: ContoursByOrientation,
    slice_ranges: Tuple[List[int], List[int], List[int]],
    axis_limits: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
    structure_names: List[StructureName],
    vmin,
    vmax,
):
    z_grid, y_grid, x_grid = grids

    colour_iterator = _get_colours()
    colours: Dict[StructureName, Tuple[float, float, float]] = {
        name: next(colour_iterator) for name in structure_names
    }

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))

    transverse_image = axs[0, 0].pcolormesh(
        x_grid,
        y_grid,
        images[slice_ranges[0][0], :, :],
        vmin=vmin,
        vmax=vmax,
        shading="nearest",
        cmap="gray",
    )

    axs[0, 0].set_aspect("equal", "box")
    axs[0, 0].set_xlim(axis_limits[2])
    axs[0, 0].set_ylim(axis_limits[1])

    def update(i):
        z_index = slice_ranges[0][i]

        transverse_image.set_array(images[z_index, :, :])

        # for structure_name, contours_by_slice in contours_by_orientation[
        #     "transverse"
        # ].items():
        #     contours = contours_by_slice[z_index]

        #     for j, contour in enumerate(contours):
        #         contour_array = np.array(contour + [contour[0]])

        #         plot_args = (
        #             contour_array[:, 0],
        #             contour_array[:, 1],
        #             # line_prop[structure_name],
        #         )
        #         plot_kwargs = {
        #             "c": colours[structure_name],
        #             # "alpha": alpha[structure_name],
        #         }

        #         # if j == 0:
        #         #     plot_kwargs["label"] = labels[structure_name]

        #         axs[0, 0].plot(*plot_args, **plot_kwargs)

        # return transverse_image

    animation = matplotlib.animation.FuncAnimation(
        fig, update, frames=len(slice_ranges[0]), interval=20, blit=True, repeat=False
    )
    ctx = {"paused": False}

    def toggle_pause(*args, **kwargs):
        if ctx["paused"]:
            animation.resume()
        else:
            animation.pause()
        ctx["paused"] = not ctx["paused"]

    fig.canvas.mpl_connect("button_press_event", toggle_pause)

    return update


class AutoScrollMasks:
    def __init__(self, cfg, grids, images, masks, vmin, vmax):
        z_grid, y_grid, x_grid = grids
        orientations = ("transverse", "coronal", "sagittal")

        orientation_axis_map = {"transverse": 0, "coronal": 1, "sagittal": 2}

        contours = {
            key: rai.masks_to_contours_by_structure(
                cfg=cfg,
                x_grid=x_grid,
                y_grid=y_grid,
                masks=masks,
                axis=orientation_axis_map[key],
            )
            for key in orientations
        }

        colour_iterator = _get_colours()
        colours: Dict[StructureName, Tuple[float, float, float]] = {
            name: next(colour_iterator) for name in cfg["structures"]
        }

        centre_indices = scipy.ndimage.center_of_mass(masks)
        visible_slice_indices = [int(np.round(item)) for item in centre_indices[0:3]]

        where_mask = np.where(masks > 127.5)
        min_mask_index = np.min(where_mask, axis=1).tolist()
        max_mask_index = np.max(where_mask, axis=1).tolist()

        self.z_slice_range = list(range(min_mask_index[0], max_mask_index[0] + 1))
        y_slice_range = [min_mask_index[1], max_mask_index[1]]
        x_slice_range = [min_mask_index[2], max_mask_index[2]]

        z_axis_range = sorted([z_grid[min_mask_index[0]], z_grid[max_mask_index[0]]])
        y_axis_range = sorted(
            [y_grid[min_mask_index[1]], y_grid[max_mask_index[1]]], reverse=True
        )
        x_axis_range = sorted([x_grid[min_mask_index[2]], x_grid[max_mask_index[2]]])

        fig, axs = plt.subplots(nrows=2, ncols=2)

        axs[0, 0].set_aspect("equal", "box")
        axs[0, 0].set_xlim(x_axis_range)
        axs[0, 0].set_ylim(y_axis_range)

        self.images = images
        self.transverse_image = axs[0, 0].pcolormesh(
            x_grid,
            y_grid,
            images[self.z_slice_range[0], :, :],
            vmin=vmin,
            vmax=vmax,
            shading="nearest",
            cmap="gray",
        )

        self.animation = animation.FuncAnimation(
            fig, self.update, frames=200, interval=50, blit=True
        )
        self.paused = False

        fig.canvas.mpl_connect("button_press_event", self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused

    def update(self, i):
        self.transverse_image.set_array = self.images[self.z_slice_range[i], :, :]

        return (self.transverse_image,)


def animate_masks(cfg, grids, images, masks, vmin, vmax):
    z_grid, y_grid, x_grid = grids

    colour_iterator = _get_colours()
    colours: Dict[StructureName, Tuple[float, float, float]] = {
        name: next(colour_iterator) for name in cfg["structures"]
    }

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

            for i, contour in enumerate(contours):
                contour_array = np.array(contour + [contour[0]])

                plot_args = (
                    contour_array[:, 0],
                    contour_array[:, 1],
                    line_prop[structure_name],
                )
                plot_kwargs = {
                    "c": colours[structure_name],
                    "alpha": alpha[structure_name],
                }

                if i == 0:
                    plot_kwargs["label"] = labels[structure_name]

                ax.plot(*plot_args, **plot_kwargs)

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

            for i, contour in enumerate(contours):
                contour_array = np.array(contour + [contour[0]])

                plot_args = (
                    contour_array[:, 0],
                    contour_array[:, 1],
                    line_prop[structure_name],
                )
                plot_kwargs = {
                    "c": colours[structure_name],
                    "alpha": alpha[structure_name],
                }

                if i == 0:
                    plot_kwargs["label"] = labels[structure_name]

                ax.plot(*plot_args, **plot_kwargs)

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
