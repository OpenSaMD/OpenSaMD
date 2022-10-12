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
from numpy.typing import NDArray
from raicontours import cfg

from rai.model import load as _load_model
from rai.typing.inference import Points

from . import batch as _batch
from . import merge as _merge


def run_inference(image_stack: NDArray[np.float32], points: Points):
    model = _load_model.load_model()

    model_input = _batch.create_batch(image_stack, points)
    model_output = model.predict(model_input)

    num_structures = len(cfg["structures"])

    merged = np.zeros(shape=image_stack.shape + (num_structures,), dtype=np.uint8)
    counts = np.zeros(shape=image_stack.shape + (1,), dtype=np.float32)
    merged, counts = _merge.merge_predictions(merged, counts, points, model_output)

    return merged
