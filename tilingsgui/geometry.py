"""[TODO]
"""

from __future__ import annotations
from typing import List
from math import cos, sin, pi


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def dist_squared_to(self, other: Point) -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


class LineSegment:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def as_vertices(self) -> List[float]:
        return [self.start.x, self.start.y, self.end.x, self.end.y]


class Rectangle:
    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def as_vertices(self) -> List[float]:
        return [
            self.x,
            self.y,
            self.x,
            self.y + self.h,
            self.x + self.w,
            self.y,
            self.x + self.w,
            self.y + self.h,
        ]

    def int_center(self) -> Point:
        return Point(self.x + self.w / 2, self.y + self.h / 2)


class Circle:
    def __init__(self, x: float, y: float, r: float) -> None:
        self.center = Point(x, y)
        self.r = r

    def as_vertices(self, splits: int = 30) -> List[float]:
        verts = [self.center.x, self.center.y]
        for i in range(splits + 1):
            ang = 2 * pi * i / splits
            verts.append(self.center.x + cos(ang) * self.r)
            verts.append(self.center.y + sin(ang) * self.r)
        return verts
