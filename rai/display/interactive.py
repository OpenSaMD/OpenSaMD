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


def draw(grids, images):
    fig = make_subplots(
        rows=2,
        cols=2,
        vertical_spacing=0.05,
        horizontal_spacing=0.05,
    )

    z_grid, y_grid, x_grid = grids
    x0, dx, _size_x, y0, dy, _size_y, z0, dz, _size_z = _get_image_params(
        x_grid, y_grid, z_grid
    )

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
            z=np.ones(shape=(len(y_grid), len(x_grid))),
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
            z=np.ones(shape=(len(z_grid), len(x_grid))),
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
            z=np.ones(shape=(len(z_grid), len(y_grid))),
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
        "spikesnap": "data",
        "spikemode": "across",
        "spikedash": "solid",
        "spikethickness": 0,
    }

    fig.update_layout(
        {
            "height": 900,
            "width": 900,
            "images": images,
            "dragmode": "pan",
            "xaxis": {"range": [-120, 150], "scaleanchor": "y", **common_axis_options},
            "yaxis": {"range": [-100, 170], **common_axis_options},
            "xaxis3": {"matches": "x", **common_axis_options},
            "yaxis3": {
                "range": [-160, 110],
                "scaleanchor": "x3",
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


def _get_image_params(x_grid, y_grid, z_grid):
    x0 = x_grid[0]
    dx = x_grid[1] - x_grid[0]
    y0 = y_grid[-1]
    dy = y_grid[-2] - y_grid[-1]
    z0 = z_grid[0]
    dz = z_grid[1] - z_grid[0]

    size_x = np.abs(x_grid[-1] - x_grid[0])
    size_y = np.abs(y_grid[-1] - y_grid[0])
    size_z = np.abs(z_grid[-1] - z_grid[0])

    return x0, dx, size_x, y0, dy, size_y, z0, dz, size_z


def _create_plotly_layout_images(grids, transverse, coronal, sagittal):
    z_grid, y_grid, x_grid = grids

    # TODO: Verification
    x0, _dx, size_x, y0, _dy, size_y, z0, _dz, size_z = _get_image_params(
        x_grid, y_grid, z_grid
    )

    images = []

    for i, img in enumerate(transverse):
        images.append(
            dict(
                name=f"transverse_{i}",
                visible=i == 50,
                source=img,
                xref="x",
                yref="y",
                x=x0,
                y=y0,
                sizex=size_x,
                sizey=size_y,
                sizing="stretch",
                # layer="below",
            )
        )

    for i, img in enumerate(coronal):
        images.append(
            dict(
                name=f"coronal_{i}",
                visible=i == 256,
                source=img,
                xref="x3",
                yref="y3",
                x=x0,
                y=z0,
                sizex=size_x,
                sizey=size_z,
                sizing="stretch",
                # layer="below",
            )
        )

    for i, img in enumerate(sagittal):
        images.append(
            dict(
                name=f"sagittal_{i}",
                visible=i == 256,
                source=img,
                xref="x4",
                yref="y4",
                x=y_grid[0],
                y=z0,
                sizex=size_y,
                sizey=size_z,
                sizing="stretch",
                # layer="below",
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
