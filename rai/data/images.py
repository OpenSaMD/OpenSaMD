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


import pathlib

import numpy as np
import pydicom
import skimage.measure
from raicontours import cfg

from rai.dicom import sorting as _dicom_sorting


def paths_to_reduced_image_stack(paths: list[pathlib.Path]):
    x_grid, y_grid, image_stack = _paths_to_image_stack_hfs(paths=paths)

    initial_reduce_block_size = cfg["reduce_block_sizes"][0]

    reduced = skimage.measure.block_reduce(
        image_stack, block_size=initial_reduce_block_size, func=np.mean
    )

    return reduced


def _paths_to_image_stack_hfs(paths: list[pathlib.Path]):
    sorted_paths = sorted(paths, key=_sorting_key)

    image_stack = []

    x_grid = None
    y_grid = None

    for path in sorted_paths:
        ds = pydicom.read_file(path)
        (
            loaded_x_grid,
            loaded_y_grid,
            model_input_image,
        ) = _get_model_dicom_grid_and_rescaled_image(ds=ds)
        x_grid, y_grid = _validate_grid(x_grid, y_grid, loaded_x_grid, loaded_y_grid)

        image_stack.append(model_input_image[None, ...])

    image_stack = np.concatenate(image_stack, axis=0)
    x_grid_hfs, y_grid_hfs, image_stack_hfs = _convert_array_to_or_from_hfs_with_grids(
        x_grid, y_grid, image_stack
    )

    return x_grid_hfs, y_grid_hfs, image_stack_hfs


def _validate_grid(x_grid_reference, y_grid_reference, x_grid, y_grid):
    if x_grid_reference is None:
        x_grid_reference = x_grid

    if y_grid_reference is None:
        y_grid_reference = y_grid

    if np.any(x_grid != x_grid_reference) or np.any(y_grid != y_grid_reference):
        raise ValueError("Inconsistent x and y grid values")

    return x_grid_reference, y_grid_reference


def _sorting_key(path: pathlib.Path):
    header = pydicom.read_file(path, force=True, stop_before_pixels=True)

    return -_dicom_sorting.slice_position(header)


def _get_model_dicom_grid_and_rescaled_image(ds: pydicom.Dataset):
    original = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
    rescaled = (original - cfg["rescale_intercept"]) / cfg["rescale_slope"]

    x_grid, y_grid = _get_grid(ds)

    return x_grid, y_grid, rescaled


def _convert_array_to_or_from_hfs_with_grids(x_grid, y_grid, array):
    """Flips the input and output along the axis where x_grid or y_grid
    is not currently always increasing.
    """
    dx = np.diff(x_grid)
    dy = np.diff(y_grid)

    flip = slice(-1, None, -1)

    if np.any(dx < 0):
        # Axes order b?, z, y, x
        array = array[..., :, flip]
        x_grid = x_grid[flip]
        dx = np.diff(x_grid)

    assert np.all(dx >= 0)

    if np.any(dy < 0):
        array = array[..., flip, :]
        y_grid = y_grid[flip]
        dy = np.diff(y_grid)

    assert np.all(dy >= 0)

    return x_grid, y_grid, array


def _get_grid(image_ds: pydicom.Dataset):
    x0, y0, dx, dy = _get_image_transformation_parameters(image_ds)

    rows, columns = _get_image_yx_size(image_ds)
    x_grid = np.linspace(x0, x0 + (columns - 1) * dx, columns)
    y_grid = np.linspace(y0, y0 + (rows - 1) * dy, rows)

    assert len(x_grid) == columns
    assert len(y_grid) == rows

    return x_grid, y_grid


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
