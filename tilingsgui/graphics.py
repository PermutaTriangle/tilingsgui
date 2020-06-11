"""A collection of drawing functions for basic shapes.
"""

from typing import Tuple
import pyglet
from .geometry import LineSegment, Circle, Rectangle

_VERTEX_MODE = "v2f"
_COLOR_MODE = "c3B"


def draw_line_segment(
    line_segment: LineSegment, color: Tuple[float, float, float]
) -> None:
    pyglet.graphics.draw(
        2,
        pyglet.gl.GL_LINE_STRIP,
        (_VERTEX_MODE, line_segment.as_vertices()),
        (_COLOR_MODE, color * 2),
    )


def draw_circle(
    circle: Circle, color: Tuple[float, float, float], splits: int = 30
) -> None:
    pyglet.graphics.draw(
        splits + 2,
        pyglet.gl.GL_TRIANGLE_FAN,
        (_VERTEX_MODE, circle.as_vertices(splits)),
        (_COLOR_MODE, color * (splits + 2)),
    )


def draw_rectangle(rectangle: Rectangle, color: Tuple[float, float, float]) -> None:
    pyglet.graphics.draw(
        4,
        pyglet.gl.GL_TRIANGLE_STRIP,
        (_VERTEX_MODE, rectangle.as_vertices()),
        (_COLOR_MODE, color * 4),
    )


def draw_segment_array():
    pass
