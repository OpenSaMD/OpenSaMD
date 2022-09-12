from .base import BaseGeometry

class Polygon(BaseGeometry):
    def __init__(self, shell: list[tuple[float, float]]) -> None: ...
