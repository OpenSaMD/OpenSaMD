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
import pathlib
from io import BytesIO

import imageio
import numpy as np
import plotly.graph_objects as go
from IPython.display import HTML, display
from plotly.subplots import make_subplots

HERE = pathlib.Path(__file__).parent
POST_SCRIPT_PATH = HERE / "plotly-post-script.js"


def draw(grids, images, ranges):
    fig = make_subplots(
        rows=2,
        cols=2,
        vertical_spacing=0.05,
        horizontal_spacing=0.05,
    )

    z_grid, y_grid, x_grid = grids
    x0, dx, y0, dy, z0, dz = _get_image_params(x_grid, y_grid, z_grid)

    common_trace_options = {
        "colorscale": "gray",
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
            **common_trace_options,
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
            **common_trace_options,
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
            **common_trace_options,
        ),
        2,
        2,
    )

    common_axis_options = {
        "constrain": "domain",
        # "showticklabels": False,
        "spikesnap": "hovered data",
        "spikemode": "across",
        "spikedash": "solid",
        "spikethickness": 0,
        "showgrid": False,
        "zeroline": False,
    }

    fig.update_layout(
        {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "height": 900,
            "width": 900,
            "images": images,
            "dragmode": "pan",
            "xaxis": {
                "range": _expand_limits(ranges[2], dx),
                "scaleanchor": "y",
                **common_axis_options,
            },
            "yaxis": {
                "range": _expand_limits(ranges[1], dy),
                **common_axis_options,
            },
            "xaxis3": {"matches": "x", **common_axis_options},
            "yaxis3": {
                "range": _expand_limits(ranges[0], dz),
                "scaleanchor": "x",
                **common_axis_options,
            },
            "yaxis4": {"matches": "y3", **common_axis_options},
            "xaxis4": {"matches": "y", **common_axis_options},
        }
    )

    with open(POST_SCRIPT_PATH, encoding="utf-8") as f:
        post_script = f.read()

    html = fig.to_html(
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
        },
        full_html=False,
        post_script=post_script,
        include_plotlyjs=True,
        validate=True,
    )

    display(HTML(html))


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


def create_plotly_layout_images(grids, visible_indices, transverse, coronal, sagittal):
    z_grid, y_grid, x_grid = grids

    # TODO: Verification
    x0, dx, y0, dy, z0, dz = _get_image_params(x_grid, y_grid, z_grid)

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
                visible=i == visible_indices[0],
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
                visible=i == visible_indices[1],
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
                visible=i == visible_indices[2],
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


def collect_slices(image_stack, vmin, vmax):
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
