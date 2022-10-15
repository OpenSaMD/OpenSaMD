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

import numba
import numpy as np
from numpy.typing import NDArray

from raicontours import Config

from . import _points, _weighting


def merge_predictions(
    cfg: Config,
    merged: NDArray[np.uint8],
    counts: NDArray[np.float32],
    points,
    model_output: NDArray[np.uint8],
):
    weighting = _weighting.create_inference_weighting(
        patch_dimensions=cfg["patch_dimensions"]
    )

    shape = merged.shape

    merged_stack_height = shape[0]
    merged_edge_length = shape[1]
    assert merged_edge_length == shape[2]

    patch_dimensions = cfg["patch_dimensions"]

    for i, point in enumerate(points):
        z, y, x = point

        z_patch_slice, z_merged_slice = _points.point_to_slices(
            point_coord=z,
            merged_size=merged_stack_height,
            patch_size=patch_dimensions[0],
        )
        y_patch_slice, y_merged_slice = _points.point_to_slices(
            point_coord=y,
            merged_size=merged_edge_length,
            patch_size=patch_dimensions[1],
        )
        x_patch_slice, x_merged_slice = _points.point_to_slices(
            point_coord=x,
            merged_size=merged_edge_length,
            patch_size=patch_dimensions[2],
        )

        float_updated_prediction, updated_counts = _update_prediction(
            prev_prediction=merged[
                z_merged_slice, y_merged_slice, x_merged_slice, :
            ].astype(np.float32),
            prev_counts=counts[z_merged_slice, y_merged_slice, x_merged_slice, :],
            new_prediction=model_output[
                i, z_patch_slice, y_patch_slice, x_patch_slice, :
            ].astype(np.float32),
            new_counts=weighting[z_patch_slice, y_patch_slice, x_patch_slice, :],
        )

        updated_prediction = np.round(float_updated_prediction).astype(np.uint8)

        merged[z_merged_slice, y_merged_slice, x_merged_slice, :] = updated_prediction
        counts[z_merged_slice, y_merged_slice, x_merged_slice, :] = updated_counts

    return merged, counts


@numba.jit(nopython=True)
def _update_prediction(
    prev_prediction: NDArray[np.float32],
    prev_counts: NDArray[np.float32],
    new_prediction: NDArray[np.float32],
    new_counts: NDArray[np.float32],
):
    updated_counts = prev_counts + new_counts

    updated_prediction: NDArray[np.float32] = (
        prev_prediction * prev_counts + new_prediction * new_counts
    ) / updated_counts

    return updated_prediction, updated_counts
