
from __future__ import annotations


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def dist_squared_to(self, other: Point) -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __iter__(self):
        yield self.x
        yield self.y
