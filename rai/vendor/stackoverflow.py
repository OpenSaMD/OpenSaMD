# This work is licensed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.
# <http://creativecommons.org/licenses/by-sa/4.0/>.

"""A collection of utilities either copied or adapted from Stack Overflow"""

from typing import Any

from numpy.typing import NDArray


# Copyright (C) EelkeSpaak <https://stackoverflow.com/users/1692028/eelkespaak>
# Adapted from https://stackoverflow.com/a/37729566/3912576
def slicing_without_array_copy(arr: NDArray[Any], a_slice: slice, axis: int):
    """Dynamically slice a numpy array without invoking a data copy"""

    multi_dim_slice = [slice(None)] * arr.ndim
    multi_dim_slice[axis] = a_slice

    return arr[tuple(multi_dim_slice)]
