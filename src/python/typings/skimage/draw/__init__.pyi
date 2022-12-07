import numpy as np
from numpy.typing import NDArray

def polygon2mask(
    image_shape: tuple[int, int], polygon: NDArray[np.float64]
) -> NDArray[np.float64]: ...
