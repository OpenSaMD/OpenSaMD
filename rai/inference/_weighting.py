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


import functools
import logging
from typing import List, Tuple

import numpy as np
import scipy.special
from numpy.typing import NDArray


@functools.lru_cache(maxsize=1)
def create_inference_weighting(patch_dimensions: Tuple[int, int, int]):
    profiles: List[NDArray[np.float32]] = []

    for length in patch_dimensions:
        profile_function = _create_profile_function(
            centre=(length - 1) / 2,
            field_width=length * 0.5,
            penumbra_width=length * 0.3,
        )

        x = np.array(range(length), dtype=np.float32)
        y = profile_function(x)

        profiles.append(y)

    weighting = (
        profiles[0][:, None, None, None]
        * profiles[1][None, :, None, None]
        * profiles[2][None, None, :, None]
    )

    logging.info(
        f"Weighting | Min {np.min(weighting)} | "
        f"Median {np.median(weighting)} | "
        f"Mean {np.mean(weighting)} | Max {np.max(weighting)}"
    )

    return weighting


def _create_profile_function(centre: float, field_width: float, penumbra_width: float):
    sig = _scaled_penumbra_sig() * penumbra_width
    mu = [centre - field_width / 2, centre + field_width / 2]

    def profile(x: NDArray[np.float32]):
        x = np.array(x, copy=False)
        return _gaussian_cdf(x, mu[0], sig) * _gaussian_cdf(
            -x, -mu[1], sig  # pylint: disable = invalid-unary-operand-type
        )

    return profile


def _scaled_penumbra_sig(profile_shoulder_edge: float = 0.8):
    sig = 1 / (2 * np.sqrt(2) * scipy.special.erfinv(profile_shoulder_edge * 2 - 1))

    return sig


def _gaussian_cdf(x: NDArray[np.float32], mu: float, sig: float):
    x = np.array(x, copy=False)
    return 0.5 * (1 + scipy.special.erf((x - mu) / (sig * np.sqrt(2))))
