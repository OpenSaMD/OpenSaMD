# Copyright (C) 2022 Radiotherapy AI Pty Ltd

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

"""Determining the Dice metric"""

import shapely.geometry.base


def from_shapely(
    a: shapely.geometry.base.BaseGeometry, b: shapely.geometry.base.BaseGeometry
) -> float:
    """Determine the Dice metric from two shapely geometries.

    Explanation of the Dice is available at:
    <https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient>

    Args:
        a (shapely.geometry.base.BaseGeometry)
        b (shapely.geometry.base.BaseGeometry)
    """

    return 2 * a.intersection(b).area / (a.area + b.area)
