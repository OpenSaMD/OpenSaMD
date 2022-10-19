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


import base64
import itertools
import pathlib
from io import BytesIO
from typing import Any, Dict, List, Tuple

import imageio
import matplotlib.cm
import numpy as np
import plotly.graph_objects as go
import scipy.ndimage
from IPython.display import HTML, display
from numpy.typing import NDArray
from plotly.subplots import make_subplots

from raicontours import Config

import rai
from rai.typing.contours import (
    AllStructuresMaskStack,
    ContoursByStructure,
    Grid,
    StructureName,
)

HERE = pathlib.Path(__file__).parent
POST_SCRIPT_PATH = HERE / "plotly-post-script.js"


def draw_contours_from_masks(
    cfg: Config,
    z_grid: Grid,
    y_grid: Grid,
    x_grid: Grid,
    image_stack,
    masks: AllStructuresMaskStack,
    vmin,
    vmax,
):
    transverse_contours = rai.masks_to_contours_by_structure(
        cfg=cfg, x_grid=x_grid, y_grid=y_grid, masks=masks, axis=0
    )
    coronal_contours = rai.masks_to_contours_by_structure(
        cfg=cfg, x_grid=x_grid, y_grid=z_grid, masks=masks, axis=1
    )
    sagittal_contours = rai.masks_to_contours_by_structure(
        cfg=cfg, x_grid=y_grid, y_grid=z_grid, masks=masks, axis=2
    )

    centre_indices = scipy.ndimage.center_of_mass(masks)
    visible_slice_indices = [int(np.round(item)) for item in centre_indices[0:3]]

    contours = {
        "transverse": transverse_contours,
        "coronal": coronal_contours,
        "sagittal": sagittal_contours,
    }

    transverse, coronal, sagittal = _collect_slices(image_stack, vmin, vmax)

    grids = (z_grid, y_grid, x_grid)
    images = _create_plotly_layout_images(
        grids, visible_slice_indices, transverse, coronal, sagittal
    )

    where_mask = np.where(masks > 127.5)
    min_mask_index = np.min(where_mask, axis=1).tolist()
    max_mask_index = np.max(where_mask, axis=1).tolist()

    z_range = sorted([z_grid[min_mask_index[0]], z_grid[max_mask_index[0]]])
    y_range = sorted(
        [y_grid[min_mask_index[1]], y_grid[max_mask_index[1]]], reverse=True
    )
    x_range = sorted([x_grid[min_mask_index[2]], x_grid[max_mask_index[2]]])

    _draw(
        cfg=cfg,
        grids=grids,
        images=images,
        ranges=[z_range, y_range, x_range],
        contours=contours,
        visible_slice_indices=visible_slice_indices,
    )


def _draw(
    cfg: Config,
    grids,
    images,
    visible_slice_indices,
    ranges,
    contours: Dict[str, ContoursByStructure],
):
    colour_iterator = _get_colours()
    colours: Dict[StructureName, str] = {
        name: next(colour_iterator) for name in cfg["structures"]
    }

    z_grid, y_grid, x_grid = grids
    x0, dx, y0, dy, z0, dz = _get_image_params(x_grid, y_grid, z_grid)

    fig = make_subplots(
        rows=2,
        cols=2,
        vertical_spacing=0.05,
        horizontal_spacing=0.05,
    )

    axis_coords = {
        "transverse": (1, 1),
        "coronal": (2, 1),
        "sagittal": (2, 2),
    }

    for orientation_index, (orientation, contours_by_structure) in enumerate(
        contours.items()
    ):
        for structure_name, contours_by_slice in contours_by_structure.items():
            for slice_index, contours_for_this_slice in enumerate(contours_by_slice):
                visible = visible_slice_indices[orientation_index] == slice_index

                for contour_index, contour in enumerate(contours_for_this_slice):
                    contour_array = np.array(contour + [contour[0]])

                    fig.add_trace(
                        go.Scatter(
                            name=f"{structure_name}, {orientation}, {slice_index}",
                            visible=visible,
                            legendgroup=structure_name,
                            x=contour_array[:, 0],
                            y=contour_array[:, 1],
                            hoverinfo="skip",
                            mode="lines",
                            marker={"color": colours[structure_name]},
                            showlegend=contour_index == 0,
                        ),
                        *axis_coords[orientation],
                    )

    common_heatmap_options = {
        "hoverinfo": "none",
        "opacity": 0,
        "showscale": False,
    }

    fig.add_trace(
        go.Heatmap(
            x0=x0,
            dx=dx,
            y0=y0,
            dy=dy,
            z=np.zeros(shape=(len(y_grid), len(x_grid))),
            name="transverse",
            xaxis="x",
            yaxis="y",
            **common_heatmap_options,
        ),
        1,
        1,
    )

    fig.add_trace(
        go.Heatmap(
            x0=x0,
            dx=dx,
            y0=z0,
            dy=dz,
            z=np.zeros(shape=(len(z_grid), len(x_grid))),
            name="coronal",
            xaxis="x3",
            yaxis="y3",
            **common_heatmap_options,
        ),
        2,
        1,
    )

    fig.add_trace(
        go.Heatmap(
            x0=y0,
            dx=dy,
            y0=z0,
            dy=dz,
            z=np.zeros(shape=(len(z_grid), len(y_grid))),
            name="sagittal",
            xaxis="x4",
            yaxis="y4",
            **common_heatmap_options,
        ),
        2,
        2,
    )

    common_axis_options = {
        # "constrain": "domain",
        # "showticklabels": False,
        "spikesnap": "hovered data",
        "spikemode": "across",
        "spikedash": "solid",
        "spikethickness": 0,
        "showgrid": False,
        "zeroline": False,
        "scaleratio": 1,
    }

    fig.update_layout(
        {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "legend": dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            "height": 1000,
            "width": 1000,
            "images": images,
            "dragmode": "pan",
            "xaxis": {
                "range": _expand_limits(ranges[2], dx),
                "scaleanchor": "y",
                **common_axis_options,
            },
            "yaxis": {
                "range": _expand_limits(ranges[1], dy),
                "matches": "x4",
                **common_axis_options,
            },
            "xaxis3": {
                "matches": "x",
                "scaleanchor": "y3",
                **common_axis_options,
            },
            "yaxis3": {
                "range": _expand_limits(ranges[0], dz),
                "matches": "y4",
                **common_axis_options,
            },
            "yaxis4": {
                **common_axis_options,
            },
            "xaxis4": {
                "scaleanchor": "y4",
                **common_axis_options,
            },
        }
    )

    with open(POST_SCRIPT_PATH, encoding="utf-8") as f:
        post_script = f.read()

    html = fig.to_html(
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": False,
        },
        full_html=False,
        post_script=post_script,
        include_plotlyjs=True,
        validate=True,
    )

    display(HTML(html))

    return fig


def _expand_limits(x_lim, dx):
    diff = x_lim[1] - x_lim[0]
    sign = np.sign(diff)
    pixel_buffer = sign * np.abs(dx) / 2

    expanded_xlim = [x_lim[0] - pixel_buffer, x_lim[1] + pixel_buffer]

    return expanded_xlim


def _get_image_params(x_grid, y_grid, z_grid):
    x0 = x_grid[0]
    dx = x_grid[1] - x_grid[0]
    y0 = y_grid[0]
    dy = y_grid[1] - y_grid[0]
    z0 = z_grid[0]
    dz = z_grid[1] - z_grid[0]

    return x0, dx, y0, dy, z0, dz


def _get_image_size_and_centre(grid):
    grid_limits = [grid[0], grid[-1]]
    dx = grid[1] - grid[0]

    expanded_limits = _expand_limits(grid_limits, dx)
    size = np.abs(expanded_limits[1] - expanded_limits[0])
    centre = np.mean(grid_limits)

    return size, centre


def _create_plotly_layout_images(
    grids, visible_slice_indices, transverse, coronal, sagittal
):
    z_grid, y_grid, x_grid = grids
    size_x, centre_x = _get_image_size_and_centre(x_grid)
    size_y, centre_y = _get_image_size_and_centre(y_grid)
    size_z, centre_z = _get_image_size_and_centre(z_grid)

    images = []

    common_image_options = {
        "xanchor": "center",
        "yanchor": "middle",
        "sizing": "stretch",
        "layer": "below",
    }

    for i, img in enumerate(transverse):
        images.append(
            dict(
                name=f"transverse_{i}",
                visible=i == visible_slice_indices[0],
                source=img,
                xref="x",
                yref="y",
                x=centre_x,
                y=centre_y,
                sizex=size_x,
                sizey=size_y,
                **common_image_options,
            )
        )

    for i, img in enumerate(coronal):
        images.append(
            dict(
                name=f"coronal_{i}",
                visible=i == visible_slice_indices[1],
                source=img,
                xref="x3",
                yref="y3",
                x=centre_x,
                y=centre_z,
                sizex=size_x,
                sizey=size_z,
                **common_image_options,
            )
        )

    for i, img in enumerate(sagittal):
        images.append(
            dict(
                name=f"sagittal_{i}",
                visible=i == visible_slice_indices[2],
                source=img,
                xref="x4",
                yref="y4",
                x=centre_y,
                y=centre_z,
                sizex=size_y,
                sizey=size_z,
                **common_image_options,
            )
        )

    return images


def _collect_slices(image_stack, vmin, vmax):
    transverse = []
    for i in range(image_stack.shape[0]):
        img = _convert_to_b64(image_stack[i, :, :], vmin, vmax)

        transverse.append(img)

    coronal = []
    for i in range(image_stack.shape[1]):
        img = _convert_to_b64(image_stack[:, i, :], vmin, vmax)

        coronal.append(img)

    sagittal = []
    for i in range(image_stack.shape[2]):
        img = _convert_to_b64(image_stack[:, -1::-1, i], vmin, vmax)

        sagittal.append(img)

    return transverse, coronal, sagittal


def _convert_to_b64(image, vmin, vmax):
    in_memory_file = BytesIO()

    scaled_img = np.round(((image - vmin) / (vmax - vmin)) * 255)
    scaled_img[scaled_img < 0] = 0
    scaled_img[scaled_img > 255] = 255
    scaled_img = scaled_img.astype(np.uint8)

    in_memory_file.seek(0)
    imageio.imsave(in_memory_file, scaled_img, format="png")
    in_memory_file.seek(0)

    raw = in_memory_file.read()
    b64 = base64.encodebytes(raw).decode()
    img = f"data:image/png;base64,{b64}"

    return img


def _get_colours():
    cmaps_to_pull_from = ["tab10", "Set3", "Set1", "Set2"]
    loaded_colours: List[Tuple[float, float, float]] = []
    for cmap in cmaps_to_pull_from:
        loaded_colours += matplotlib.cm.get_cmap(cmap).colors

    np_colours: NDArray[np.uint8] = np.round(np.array(loaded_colours) * 255).astype(
        np.uint8
    )

    greys_ref = np.logical_and(
        np.abs(np_colours[:, 0] - np_colours[:, 1]) < 30,
        np.abs(np_colours[:, 0] - np_colours[:, 2]) < 30,
        np.abs(np_colours[:, 1] - np_colours[:, 2]) < 30,
    )
    np_colours = np_colours[np.invert(greys_ref)]

    rgb_string_colours = [f"rgb({item[0]},{item[1]},{item[2]})" for item in np_colours]

    return itertools.cycle(rgb_string_colours)
