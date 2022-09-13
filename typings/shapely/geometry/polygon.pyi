from numpy.typing import NDArray
from typing import Any, Optional, Union

from .base import BaseGeometry

class Polygon(BaseGeometry):
    def __init__(
        self, shell: Optional[Union[list[tuple[float, float]], NDArray[Any]]] = ...
    ) -> None: ...
