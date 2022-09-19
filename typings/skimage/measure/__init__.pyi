from typing import Any, Callable

import numpy as np
from numpy.typing import NDArray

def find_contours(image: NDArray[Any], level: float) -> NDArray[np.float64]: ...
def block_reduce(
    image: NDArray[Any],
    block_size: tuple[int, ...],
    func: Callable[[NDArray[Any]], NDArray[Any]],
) -> NDArray[np.float64]: ...
