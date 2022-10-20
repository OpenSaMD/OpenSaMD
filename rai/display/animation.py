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
from matplotlib.axes import Axes

from rai.typing.contours import (
    ContoursByOrientation,
    ContoursByStructure,
    ContoursXY,
    Grid,
    Orienation,
    StructureName,
)
from rai.vendor.stackoverflow import slicing_without_array_copy

ORIENTATION_TO_AXIS: Dict[Orienation, int] = {
    "transverse": 0,
    "coronal": 1,
    "sagittal": 2,
}


def view_ranges_from_masks(grids, masks, buffer=0.1):
    where_mask = np.where(masks > 127.5)
    min_mask_index = np.min(where_mask, axis=1).tolist()
    max_mask_index = np.max(where_mask, axis=1).tolist()

    slice_indices = tuple(
        (
            list(range(min_mask_index[axis], max_mask_index[axis] + 1))
            for axis in range(3)
        )
    )

    axis_reverse = [False, True, False]

    axis_limits = []
    for axis, reverse in enumerate(axis_reverse):
        lim_a = grids[axis][min_mask_index[axis]]
        lim_b = grids[axis][max_mask_index[axis]]

        limit_range = np.abs(lim_b - lim_a)
        expansion = buffer * limit_range

        sorted_limits = sorted([lim_a, lim_b])
        sorted_limits[0] = sorted_limits[0] - expansion
        sorted_limits[1] = sorted_limits[1] + expansion

        if reverse:
            sorted_limits = [sorted_limits[1], sorted_limits[0]]

        axis_limits.append(tuple(sorted_limits))

    centre_indices = [
        int(np.round(item)) for item in scipy.ndimage.center_of_mass(masks)[0:3]
    ]

    return slice_indices, tuple(axis_limits), centre_indices


def plot_contours_by_structure(
    grids,
    images,
    contours_by_structure: ContoursByStructure,
    orientation: Orienation,
    slice_indices,
    axis_limits,
    structure_names,
    figsize,
    vmin,
    vmax,
):
    z_grid, y_grid, x_grid = grids
    colour_iterator = _get_colours()
    colours: Dict[StructureName, Tuple[float, float, float]] = {
        name: next(colour_iterator) for name in structure_names
    }

    orientation_specific_params = {
        "transverse": {
            "x_grid": x_grid,
            "y_grid": y_grid,
        },
        "coronal": {
            "x_grid": x_grid,
            "y_grid": z_grid,
        },
        "sagittal": {
            "x_grid": y_grid,
            "y_grid": z_grid,
        },
    }

    orientation_specific_limits = {
        "transverse": {
            "xlim": axis_limits[2],
            "ylim": axis_limits[1],
        },
        "coronal": {
            "xlim": axis_limits[2],
            "ylim": axis_limits[0],
        },
        "sagittal": {
            "xlim": axis_limits[1],
            "ylim": axis_limits[0],
        },
    }

    axis = ORIENTATION_TO_AXIS[orientation]
    for i in slice_indices[axis]:
        fig, ax = plt.subplots(figsize=figsize)
        _populate_axis_for_orientation_and_index(
            ax=ax,
            images=images,
            contours_by_structure=contours_by_structure,
            colours=colours,
            vmin=vmin,
            vmax=vmax,
            orientation=orientation,
            index=i,
            **orientation_specific_params[orientation]
        )
        ax.set_xlim(*orientation_specific_limits[orientation]["xlim"])
        ax.set_ylim(*orientation_specific_limits[orientation]["ylim"])

        plt.show()


def auto_scroll_contours_by_orientation(
    grids: Tuple[Grid, Grid, Grid],
    images,
    contours_by_orientation: ContoursByOrientation,
    slice_indicies: Tuple[List[int], List[int], List[int]],
    axis_limits: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
    structure_names: List[StructureName],
    vmin,
    vmax,
    interval,
):
    z_grid, y_grid, x_grid = grids

    colour_iterator = _get_colours()
    colours: Dict[StructureName, Tuple[float, float, float]] = {
        name: next(colour_iterator) for name in structure_names
    }

    fig = plt.figure(constrained_layout=True, figsize=(12, 12))
    gs = fig.add_gridspec(2, 2)

    axs: Dict[Orienation, Axes] = {
        "transverse": fig.add_subplot(gs[0, :]),
        "coronal": fig.add_subplot(gs[1, 0]),
        "sagittal": fig.add_subplot(gs[1, 1]),
    }

    orientation_specific_params = {
        "transverse": {
            "x_grid": x_grid,
            "y_grid": y_grid,
        },
        "coronal": {
            "x_grid": x_grid,
            "y_grid": z_grid,
        },
        "sagittal": {
            "x_grid": y_grid,
            "y_grid": z_grid,
        },
    }

    orientation_specific_limits = {
        "transverse": {
            "xlim": axis_limits[2],
            "ylim": axis_limits[1],
        },
        "coronal": {
            "xlim": axis_limits[2],
            "ylim": axis_limits[0],
        },
        "sagittal": {
            "xlim": axis_limits[1],
            "ylim": axis_limits[0],
        },
    }

    image_patches = {}
    contour_patches = {}
    for orientation, ax in axs.items():
        axis = ORIENTATION_TO_AXIS[orientation]
        image_patch, contour_patch = _populate_axis_for_orientation_and_index(
            ax=ax,
            images=images,
            contours_by_structure=contours_by_orientation[orientation],
            colours=colours,
            vmin=vmin,
            vmax=vmax,
            orientation=orientation,
            index=slice_indicies[axis][0],
            **orientation_specific_params[orientation]
        )

        image_patches[orientation] = image_patch
        contour_patches[orientation] = contour_patch

        ax.set_xlim(*orientation_specific_limits[orientation]["xlim"])
        ax.set_ylim(*orientation_specific_limits[orientation]["ylim"])

    # plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    animation_index_conversion = []
    for orientation, axis in ORIENTATION_TO_AXIS.items():
        index_pair = [(orientation, index) for index in slice_indicies[axis]]
        animation_index_conversion += index_pair

    def update(animation_index):
        orientation, slice_index = animation_index_conversion[animation_index]
        axis = ORIENTATION_TO_AXIS[orientation]

        image = slicing_without_array_copy(
            images, slice(slice_index, slice_index + 1), axis
        )
        image = np.squeeze(image, axis=axis)
        image_patches[orientation].set_array(image)

        for structure_name, contour_patch in contour_patches[orientation].items():
            contours_by_slice = contours_by_orientation[orientation][structure_name]
            contours = _combine_contours_for_plotting(contours_by_slice[slice_index])

            contour_patch.set_xdata(contours[:, 0])
            contour_patch.set_ydata(contours[:, 1])

    animation = matplotlib.animation.FuncAnimation(
        fig,
        update,
        frames=len(animation_index_conversion),
        interval=interval,
        repeat=False,
    )
    ctx = {"paused": False}

    def toggle_pause(*_args, **_kwargs):
        if ctx["paused"]:
            animation.resume()
        else:
            animation.pause()
        ctx["paused"] = not ctx["paused"]

    fig.canvas.mpl_connect("button_press_event", toggle_pause)


def _populate_axis_for_orientation_and_index(
    ax: Axes,
    x_grid,
    y_grid,
    images,
    contours_by_structure: ContoursByStructure,
    colours,
    vmin,
    vmax,
    orientation: Orienation,
    index: int,
):
    axis = ORIENTATION_TO_AXIS[orientation]

    image = slicing_without_array_copy(images, slice(index, index + 1), axis)
    image = np.squeeze(image, axis=axis)

    image_trace = ax.pcolormesh(
        x_grid,
        y_grid,
        image,
        vmin=vmin,
        vmax=vmax,
        shading="nearest",
        cmap="gray",
    )

    contour_traces_by_structure = {}
    for structure_name, contours_by_slice in contours_by_structure.items():
        contours = _combine_contours_for_plotting(contours_by_slice[index])

        plot_args = (contours[:, 0], contours[:, 1])
        plot_kwargs = {
            "c": colours[structure_name],
            "label": structure_name,
        }

        (contour_traces_by_structure[structure_name],) = ax.plot(
            *plot_args, **plot_kwargs
        )

    ax.set_aspect("equal", "box")

    return image_trace, contour_traces_by_structure


def _combine_contours_for_plotting(contours: ContoursXY):
    contour_arrays = []
    for contour in contours:
        contour_arrays.append(np.array(contour + [contour[0]]))

    combined_contours: ContoursXY = [[(np.nan, np.nan)]] * (len(contour_arrays) * 2 - 1)
    combined_contours[0::2] = contour_arrays

    try:
        merged_contour_arrays = np.concatenate(combined_contours, axis=0)
    except ValueError:
        merged_contour_arrays = np.array([[np.nan, np.nan]])

    return merged_contour_arrays


def _get_colours():
    cmaps_to_pull_from = ["tab10", "Set3", "Set1", "Set2"]
    loaded_colours = []
    for cmap in cmaps_to_pull_from:
        loaded_colours += matplotlib.cm.get_cmap(cmap).colors  # type: ignore

    colours = np.array(loaded_colours)  # type: ignore

    greys_ref = np.logical_and(
        np.abs(colours[:, 0] - colours[:, 1]) < 0.1,  # type: ignore
        np.abs(colours[:, 0] - colours[:, 2]) < 0.1,  # type: ignore
        np.abs(colours[:, 1] - colours[:, 2]) < 0.1,  # type: ignore
    )
    colours: np.ndarray = colours[np.invert(greys_ref)]  # type: ignore
    colours: List[Tuple[float, float, float]] = [tuple(item) for item in colours]

    return itertools.cycle(colours)
