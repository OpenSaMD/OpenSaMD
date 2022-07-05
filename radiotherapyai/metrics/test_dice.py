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

import numpy as np
import shapely.geometry

from .dice import dice_from_polygons


def test_dice_from_polygons():
    cases = [
        {
            "label": "Two unit squares with 50% overlap",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(0.5, 0), (0.5, 1), (1.5, 1), (1.5, 0)],
            "expected_dice": 2 * 0.5 / (1 + 1),
        },
        {
            "label": "Two unit squares with no overlap",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(1, 0), (1, 1), (1, 1), (1, 0)],
            "expected_dice": 0,
        },
        {
            "label": "Two unit squares with 100% overlap",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "expected_dice": 1,
        },
        {
            "label": "Squares with different area",
            "a": [(0, 0), (0, 1), (1, 1), (1, 0)],
            "b": [(0, 0), (0, 2), (2, 2), (2, 0)],
            "expected_dice": 2 * 1 / (1 + 4),
        },
    ]

    for case in cases:
        a = shapely.geometry.polygon.Polygon(case["a"])
        b = shapely.geometry.polygon.Polygon(case["b"])

        returned_dice = dice_from_polygons(a, b)

        assert np.isclose(returned_dice, case["expected_dice"]), case["label"]
