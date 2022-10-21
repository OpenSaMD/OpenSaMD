# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2021-2022 Radiotherapy AI Holdings Pty Ltd

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

from __future__ import annotations

import pathlib
from typing import List

import numpy as np
import pydicom
from numpy.typing import NDArray

from raicontours import Config

from rai.typing.contours import Grid
from rai.vendor.innolitics import sorting as _dicom_sorting


def paths_to_sorted_image_series(paths: List[pathlib.Path]):
    datasets = [pydicom.read_file(path) for path in paths]
    sorted_image_series = sorted(datasets, key=_sorting_key)

    return sorted_image_series


def sorted_image_series_to_image_stack_hfs(cfg: Config, sorted_image_series):
    image_stack = []

    x_grid = None
    y_grid = None
    z_grid = []

    for ds in sorted_image_series:
        (
            loaded_x_grid,
            loaded_y_grid,
            model_input_image,
        ) = _get_model_dicom_grid_and_rescaled_image(cfg=cfg, ds=ds)
        x_grid, y_grid = _validate_grid(x_grid, y_grid, loaded_x_grid, loaded_y_grid)

        image_stack.append(model_input_image[None, ...])
        z_grid.append(float(ds.ImagePositionPatient[-1]))

    image_stack = np.concatenate(image_stack, axis=0)
    x_grid_hfs, y_grid_hfs, image_stack_hfs = _convert_array_to_or_from_hfs_with_grids(
        x_grid, y_grid, image_stack  # type: ignore
    )

    grids = (z_grid, y_grid_hfs, x_grid_hfs)

    return grids, image_stack_hfs


def _validate_grid(x_grid_reference, y_grid_reference, x_grid, y_grid):
    if x_grid_reference is None:
        x_grid_reference = x_grid

    if y_grid_reference is None:
        y_grid_reference = y_grid

    if np.any(x_grid != x_grid_reference) or np.any(y_grid != y_grid_reference):
        raise ValueError("Inconsistent x and y grid values")

    return x_grid_reference, y_grid_reference


def _sorting_key(ds: pydicom.Dataset):
    return -_dicom_sorting.slice_position(ds)


def _get_model_dicom_grid_and_rescaled_image(cfg: Config, ds: pydicom.Dataset):
    original = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
    rescaled = (original - cfg["rescale_intercept"]) / cfg["rescale_slope"]

    x_grid, y_grid = _get_grid(ds)

    return x_grid, y_grid, rescaled


def _convert_array_to_or_from_hfs_with_grids(
    x_grid: Grid, y_grid: Grid, array: NDArray[np.float32]
):
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

    orientations_that_should_be_unit_magnitude = (
        orientation[0],
        orientation[4],
    )

    zero_pass = np.allclose(orientations_that_should_be_zero, (0, 0, 0, 0))
    unit_pass = np.allclose(np.abs(orientations_that_should_be_unit_magnitude), (1, 1))

    if not zero_pass or not unit_pass:
        raise ValueError(
            "Unsupported orientation, required one of HFS, HFP, FFS, or FFP. "
            f"The ImageOrientationPatient was {orientation}."
        )

    dx = spacing[0] * orientation[0]
    dy = spacing[1] * orientation[4]

    x0, y0, _z0 = position

    return x0, y0, dx, dy


def _get_image_yx_size(image_ds: pydicom.Dataset):
    return (image_ds.Rows, image_ds.Columns)
