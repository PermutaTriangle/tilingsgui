from __future__ import annotations

from typing import Iterable


class Point:
    """A two dimensional position.
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def dist_squared_to(self, other: Point) -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def coords(self) -> Iterable[float]:
        yield self.x
        yield self.y


class Rectangle:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def center(self) -> Point:
        return Point(self.x + self.w / 2, self.y + self.h / 2)
