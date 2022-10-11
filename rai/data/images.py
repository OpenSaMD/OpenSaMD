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
import pydicom
from raicontours import cfg


def get_model_input_image(ds: pydicom.Dataset):
    original = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
    rescaled = (
        cfg["pixel_value_factor"]
        * (original - cfg["rescale_intercept"])
        / cfg["rescale_slope"]
    )

    x_grid, y_grid = _get_grid(ds)

    model_input_image = _convert_array_to_or_from_hfs_with_grids(
        x_grid, y_grid, rescaled
    ).astype("float32")

    return x_grid, y_grid, model_input_image


def _get_grid(image_ds: pydicom.Dataset):
    x0, y0, dx, dy = _get_image_transformation_parameters(image_ds)

    rows, columns = _get_image_yx_size(image_ds)
    x_grid = np.linspace(x0, x0 + (columns - 1) * dx, columns)
    y_grid = np.linspace(y0, y0 + (rows - 1) * dy, rows)

    assert len(x_grid) == columns
    assert len(y_grid) == rows

    return x_grid, y_grid


def _convert_array_to_or_from_hfs_with_grids(x_grid, y_grid, array):
    """Flips the input and output along the axis where x_grid or y_grid
    is not currently always increasing.

    Note
    ----
    Throughout the codebase x_grid and y_grid always correspond to
    the patient coordinates that are exported from the original dicom
    image slice. Right before the data is passed through to the model
    the input and output arrays are adjusted so that the image is
    presented as if the patient was in HFS orientation. This is so that
    ant is always at the top of the image, post at the bottom,
    patient left at the right of the image and patient right at the
    left of the image.

    Before any inference occurs the input image needs to be flipped into
    HFS orientation, and then the final mask produced needs to be
    flipped back to match.

    """
    dx = np.diff(x_grid)
    dy = np.diff(y_grid)

    flip = slice(-1, None, -1)

    if np.any(dx < 0):
        # Axes order z, y, x, c
        array = array[:, :, flip, :]
        dx = np.diff(x_grid[flip])

    assert np.all(dx >= 0)

    if np.any(dy < 0):
        array = array[:, flip, :, :]
        dy = np.diff(y_grid[flip])

    assert np.all(dy >= 0)

    array_hfs: np.ndarray = array

    return array_hfs


def _get_image_transformation_parameters(image_ds: pydicom.Dataset):
    position = image_ds.ImagePositionPatient
    spacing = image_ds.PixelSpacing
    orientation = image_ds.ImageOrientationPatient

    orientations_that_should_be_zero = (
        orientation[1],
        orientation[2],
        orientation[3],
        orientation[5],
    )

    if not np.allclose(orientations_that_should_be_zero, (0, 0, 0, 0)):
        raise ValueError(
            "Unsupported orientation, required one of HFS, HFP, FFS, or FFP. "
            f"The ImageOrientationPatient was {orientation}."
        )

    dx = spacing[0] * orientation[0]
    dy = spacing[1] * orientation[1]

    x0, y0, _z0 = position

    return x0, y0, dx, dy


def _get_image_yx_size(image_ds: pydicom.Dataset):
    return (image_ds.Rows, image_ds.Columns)
