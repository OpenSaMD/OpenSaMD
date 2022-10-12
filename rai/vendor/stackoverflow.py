# This work is licensed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.
# <http://creativecommons.org/licenses/by-sa/4.0/>.

# https://stackoverflow.com/help/licensing

"""A collection of utilities either copied or adapted from Stack Overflow"""

from typing import Any

from numpy.typing import NDArray


# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
# Copyright (C) 2016,2019 EelkeSpaak <https://stackoverflow.com/users/1692028/eelkespaak>
# Timeline https://stackoverflow.com/posts/37729566/timeline
# Adapted from https://stackoverflow.com/a/37729566/3912576
def slicing_without_array_copy(arr: NDArray[Any], a_slice: slice, axis: int):
    """Dynamically slice a numpy array without invoking a data copy"""

    multi_dim_slice = [slice(None)] * arr.ndim
    multi_dim_slice[axis] = a_slice

    return arr[tuple(multi_dim_slice)]
