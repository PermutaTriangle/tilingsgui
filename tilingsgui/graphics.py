"""Drawable objects
"""

from __future__ import annotations
from typing import Tuple, List, ClassVar
from math import cos, sin, pi
from abc import ABC, abstractmethod
import pyglet


class Drawable(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class with
    """

    _VERTEX_MODE: ClassVar[str] = "v2f"
    _COLOR_MODE: ClassVar[str] = "c3B"

    @abstractmethod
    def draw(self, color: Tuple[float, ...]) -> None:
        """Draw the object.

        Args:
            color (Tuple[float, ...]): color value for drawing.
        """


class Point:
    """A 2d point.
    """

    def __init__(self, x: float, y: float) -> None:
        """[TODO]

        Args:
            x (float): x coordinate
            y (float): y coordinate
        """
        self.x = x
        self.y = y

    def dist_squared_to(self, other: Point) -> float:
        """TODO

        Args:
            other (Point): [TODO]

        Returns:
            float: [TODO]
        """
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __iter__(self):
        yield self.x
        yield self.y


class LineSegment(Drawable):
    """A 2d line segment.
    """

    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """[TODO]

        Args:
            x1 (float): [TODO]
            y1 (float): [TODO]
            x2 (float): [TODO]
            y2 (float): [TODO]
        """
        self.start: Point = Point(x1, y1)
        self.end: Point = Point(x2, y2)

    def as_vertices(self) -> List[float]:
        """[TODO]

        Returns:
            List[float]: [TODO]
        """
        return [self.start.x, self.start.y, self.end.x, self.end.y]

    def draw(self, color: Tuple[float, ...]) -> None:
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINE_STRIP,
            (Drawable._VERTEX_MODE, self.as_vertices()),
            (Drawable._COLOR_MODE, color * 2),
        )


class Rectangle(Drawable):
    """[TODO]
    """

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        """[TODO]

        Args:
            x (float): [TODO]
            y (float): [TODO]
            w (float): [TODO]
            h (float): [TODO]
        """
        self.x: float = x
        self.y: float = y
        self.w: float = w
        self.h: float = h

    def as_vertices(self) -> List[float]:
        """[TODO]

        Returns:
            List[float]: [TODO]
        """
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

    def draw(self, color: Tuple[float, ...]) -> None:
        pyglet.graphics.draw(
            4,
            pyglet.gl.GL_TRIANGLE_STRIP,
            (Drawable._VERTEX_MODE, self.as_vertices()),
            (Drawable._COLOR_MODE, color * 4),
        )


class Circle(Drawable):
    """[TODO]
    """

    def __init__(self, x: float, y: float, r: float) -> None:
        """[TODO]

        Args:
            x (float): [TODO]
            y (float): [TODO]
            r (float): [TODO]
        """
        self.center: Point = Point(x, y)
        self.r: float = r

    def as_vertices(self) -> List[float]:
        """[TODO]

        Returns:
            List[float]: [TODO]
        """
        verts = [self.center.x, self.center.y]
        for i in range(31):
            ang = 2 * pi * i / 30
            verts.append(self.center.x + cos(ang) * self.r)
            verts.append(self.center.y + sin(ang) * self.r)
        return verts

    def draw(self, color: Tuple[float, ...]) -> None:
        pyglet.graphics.draw(
            32,
            pyglet.gl.GL_TRIANGLE_FAN,
            (Drawable._VERTEX_MODE, self.as_vertices()),
            (Drawable._COLOR_MODE, color * 32),
        )


class PointPath(Drawable):
    """[TODO]

    Args:
        Drawable ([type]): [TODO]
    """

    def __init__(self, pnts: List[Point]):
        """[TODO]

        Args:
            pnts (List[Point]): [TODO]
        """
        self.path: List[Point] = pnts

    def as_vertices(self) -> List[float]:
        """[TODO]

        Returns:
            List[float]: [TODO]
        """
        return [coordinate for pnt in self.path for coordinate in pnt]

    def draw(self, color: Tuple[float, ...]) -> None:
        n = len(self.path)
        pyglet.graphics.draw(
            n,
            pyglet.gl.GL_LINE_STRIP,
            (Drawable._VERTEX_MODE, self.as_vertices()),
            (Drawable._COLOR_MODE, color * n),
        )

    def append(self, point: Point) -> None:
        """[Todo]

        Args:
            point (Point): [Todo]
        """
        self.path.append(point)


class Color:
    """A collection of color constants.
    """

    # Scraped with bs4 from https://www.rapidtables.com/web/color/RGB_Color.html.

    MAROON: ClassVar[Tuple[int, int, int]] = (128, 0, 0)
    DARK_RED: ClassVar[Tuple[int, int, int]] = (139, 0, 0)
    BROWN: ClassVar[Tuple[int, int, int]] = (165, 42, 42)
    FIREBRICK: ClassVar[Tuple[int, int, int]] = (178, 34, 34)
    CRIMSON: ClassVar[Tuple[int, int, int]] = (220, 20, 60)
    RED: ClassVar[Tuple[int, int, int]] = (255, 0, 0)
    TOMATO: ClassVar[Tuple[int, int, int]] = (255, 99, 71)
    CORAL: ClassVar[Tuple[int, int, int]] = (255, 127, 80)
    INDIAN_RED: ClassVar[Tuple[int, int, int]] = (205, 92, 92)
    LIGHT_CORAL: ClassVar[Tuple[int, int, int]] = (240, 128, 128)
    DARK_SALMON: ClassVar[Tuple[int, int, int]] = (233, 150, 122)
    SALMON: ClassVar[Tuple[int, int, int]] = (250, 128, 114)
    LIGHT_SALMON: ClassVar[Tuple[int, int, int]] = (255, 160, 122)
    ORANGE_RED: ClassVar[Tuple[int, int, int]] = (255, 69, 0)
    DARK_ORANGE: ClassVar[Tuple[int, int, int]] = (255, 140, 0)
    ORANGE: ClassVar[Tuple[int, int, int]] = (255, 165, 0)
    GOLD: ClassVar[Tuple[int, int, int]] = (255, 215, 0)
    DARK_GOLDEN_ROD: ClassVar[Tuple[int, int, int]] = (184, 134, 11)
    GOLDEN_ROD: ClassVar[Tuple[int, int, int]] = (218, 165, 32)
    PALE_GOLDEN_ROD: ClassVar[Tuple[int, int, int]] = (238, 232, 170)
    DARK_KHAKI: ClassVar[Tuple[int, int, int]] = (189, 183, 107)
    KHAKI: ClassVar[Tuple[int, int, int]] = (240, 230, 140)
    OLIVE: ClassVar[Tuple[int, int, int]] = (128, 128, 0)
    YELLOW: ClassVar[Tuple[int, int, int]] = (255, 255, 0)
    YELLOW_GREEN: ClassVar[Tuple[int, int, int]] = (154, 205, 50)
    DARK_OLIVE_GREEN: ClassVar[Tuple[int, int, int]] = (85, 107, 47)
    OLIVE_DRAB: ClassVar[Tuple[int, int, int]] = (107, 142, 35)
    LAWN_GREEN: ClassVar[Tuple[int, int, int]] = (124, 252, 0)
    CHART_REUSE: ClassVar[Tuple[int, int, int]] = (127, 255, 0)
    GREEN_YELLOW: ClassVar[Tuple[int, int, int]] = (173, 255, 47)
    DARK_GREEN: ClassVar[Tuple[int, int, int]] = (0, 100, 0)
    GREEN: ClassVar[Tuple[int, int, int]] = (0, 128, 0)
    FOREST_GREEN: ClassVar[Tuple[int, int, int]] = (34, 139, 34)
    LIME: ClassVar[Tuple[int, int, int]] = (0, 255, 0)
    LIME_GREEN: ClassVar[Tuple[int, int, int]] = (50, 205, 50)
    LIGHT_GREEN: ClassVar[Tuple[int, int, int]] = (144, 238, 144)
    PALE_GREEN: ClassVar[Tuple[int, int, int]] = (152, 251, 152)
    DARK_SEA_GREEN: ClassVar[Tuple[int, int, int]] = (143, 188, 143)
    MEDIUM_SPRING_GREEN: ClassVar[Tuple[int, int, int]] = (0, 250, 154)
    SPRING_GREEN: ClassVar[Tuple[int, int, int]] = (0, 255, 127)
    SEA_GREEN: ClassVar[Tuple[int, int, int]] = (46, 139, 87)
    MEDIUM_AQUA_MARINE: ClassVar[Tuple[int, int, int]] = (102, 205, 170)
    MEDIUM_SEA_GREEN: ClassVar[Tuple[int, int, int]] = (60, 179, 113)
    LIGHT_SEA_GREEN: ClassVar[Tuple[int, int, int]] = (32, 178, 170)
    DARK_SLATE_GRAY: ClassVar[Tuple[int, int, int]] = (47, 79, 79)
    TEAL: ClassVar[Tuple[int, int, int]] = (0, 128, 128)
    DARK_CYAN: ClassVar[Tuple[int, int, int]] = (0, 139, 139)
    AQUA: ClassVar[Tuple[int, int, int]] = (0, 255, 255)
    CYAN: ClassVar[Tuple[int, int, int]] = (0, 255, 255)
    LIGHT_CYAN: ClassVar[Tuple[int, int, int]] = (224, 255, 255)
    DARK_TURQUOISE: ClassVar[Tuple[int, int, int]] = (0, 206, 209)
    TURQUOISE: ClassVar[Tuple[int, int, int]] = (64, 224, 208)
    MEDIUM_TURQUOISE: ClassVar[Tuple[int, int, int]] = (72, 209, 204)
    PALE_TURQUOISE: ClassVar[Tuple[int, int, int]] = (175, 238, 238)
    AQUA_MARINE: ClassVar[Tuple[int, int, int]] = (127, 255, 212)
    POWDER_BLUE: ClassVar[Tuple[int, int, int]] = (176, 224, 230)
    CADET_BLUE: ClassVar[Tuple[int, int, int]] = (95, 158, 160)
    STEEL_BLUE: ClassVar[Tuple[int, int, int]] = (70, 130, 180)
    CORN_FLOWER_BLUE: ClassVar[Tuple[int, int, int]] = (100, 149, 237)
    DEEP_SKY_BLUE: ClassVar[Tuple[int, int, int]] = (0, 191, 255)
    DODGER_BLUE: ClassVar[Tuple[int, int, int]] = (30, 144, 255)
    LIGHT_BLUE: ClassVar[Tuple[int, int, int]] = (173, 216, 230)
    SKY_BLUE: ClassVar[Tuple[int, int, int]] = (135, 206, 235)
    LIGHT_SKY_BLUE: ClassVar[Tuple[int, int, int]] = (135, 206, 250)
    MIDNIGHT_BLUE: ClassVar[Tuple[int, int, int]] = (25, 25, 112)
    NAVY: ClassVar[Tuple[int, int, int]] = (0, 0, 128)
    DARK_BLUE: ClassVar[Tuple[int, int, int]] = (0, 0, 139)
    MEDIUM_BLUE: ClassVar[Tuple[int, int, int]] = (0, 0, 205)
    BLUE: ClassVar[Tuple[int, int, int]] = (0, 0, 255)
    ROYAL_BLUE: ClassVar[Tuple[int, int, int]] = (65, 105, 225)
    BLUE_VIOLET: ClassVar[Tuple[int, int, int]] = (138, 43, 226)
    INDIGO: ClassVar[Tuple[int, int, int]] = (75, 0, 130)
    DARK_SLATE_BLUE: ClassVar[Tuple[int, int, int]] = (72, 61, 139)
    SLATE_BLUE: ClassVar[Tuple[int, int, int]] = (106, 90, 205)
    MEDIUM_SLATE_BLUE: ClassVar[Tuple[int, int, int]] = (123, 104, 238)
    MEDIUM_PURPLE: ClassVar[Tuple[int, int, int]] = (147, 112, 219)
    DARK_MAGENTA: ClassVar[Tuple[int, int, int]] = (139, 0, 139)
    DARK_VIOLET: ClassVar[Tuple[int, int, int]] = (148, 0, 211)
    DARK_ORCHID: ClassVar[Tuple[int, int, int]] = (153, 50, 204)
    MEDIUM_ORCHID: ClassVar[Tuple[int, int, int]] = (186, 85, 211)
    PURPLE: ClassVar[Tuple[int, int, int]] = (128, 0, 128)
    THISTLE: ClassVar[Tuple[int, int, int]] = (216, 191, 216)
    PLUM: ClassVar[Tuple[int, int, int]] = (221, 160, 221)
    VIOLET: ClassVar[Tuple[int, int, int]] = (238, 130, 238)
    MAGENTA: ClassVar[Tuple[int, int, int]] = (255, 0, 255)
    ORCHID: ClassVar[Tuple[int, int, int]] = (218, 112, 214)
    MEDIUM_VIOLET_RED: ClassVar[Tuple[int, int, int]] = (199, 21, 133)
    PALE_VIOLET_RED: ClassVar[Tuple[int, int, int]] = (219, 112, 147)
    DEEP_PINK: ClassVar[Tuple[int, int, int]] = (255, 20, 147)
    HOT_PINK: ClassVar[Tuple[int, int, int]] = (255, 105, 180)
    LIGHT_PINK: ClassVar[Tuple[int, int, int]] = (255, 182, 193)
    PINK: ClassVar[Tuple[int, int, int]] = (255, 192, 203)
    ANTIQUE_WHITE: ClassVar[Tuple[int, int, int]] = (250, 235, 215)
    BEIGE: ClassVar[Tuple[int, int, int]] = (245, 245, 220)
    BISQUE: ClassVar[Tuple[int, int, int]] = (255, 228, 196)
    BLANCHED_ALMOND: ClassVar[Tuple[int, int, int]] = (255, 235, 205)
    WHEAT: ClassVar[Tuple[int, int, int]] = (245, 222, 179)
    CORN_SILK: ClassVar[Tuple[int, int, int]] = (255, 248, 220)
    LEMON_CHIFFON: ClassVar[Tuple[int, int, int]] = (255, 250, 205)
    LIGHT_GOLDEN_ROD_YELLOW: ClassVar[Tuple[int, int, int]] = (250, 250, 210)
    LIGHT_YELLOW: ClassVar[Tuple[int, int, int]] = (255, 255, 224)
    SADDLE_BROWN: ClassVar[Tuple[int, int, int]] = (139, 69, 19)
    SIENNA: ClassVar[Tuple[int, int, int]] = (160, 82, 45)
    CHOCOLATE: ClassVar[Tuple[int, int, int]] = (210, 105, 30)
    PERU: ClassVar[Tuple[int, int, int]] = (205, 133, 63)
    SANDY_BROWN: ClassVar[Tuple[int, int, int]] = (244, 164, 96)
    BURLY_WOOD: ClassVar[Tuple[int, int, int]] = (222, 184, 135)
    TAN: ClassVar[Tuple[int, int, int]] = (210, 180, 140)
    ROSY_BROWN: ClassVar[Tuple[int, int, int]] = (188, 143, 143)
    MOCCASIN: ClassVar[Tuple[int, int, int]] = (255, 228, 181)
    NAVAJO_WHITE: ClassVar[Tuple[int, int, int]] = (255, 222, 173)
    PEACH_PUFF: ClassVar[Tuple[int, int, int]] = (255, 218, 185)
    MISTY_ROSE: ClassVar[Tuple[int, int, int]] = (255, 228, 225)
    LAVENDER_BLUSH: ClassVar[Tuple[int, int, int]] = (255, 240, 245)
    LINEN: ClassVar[Tuple[int, int, int]] = (250, 240, 230)
    OLD_LACE: ClassVar[Tuple[int, int, int]] = (253, 245, 230)
    PAPAYA_WHIP: ClassVar[Tuple[int, int, int]] = (255, 239, 213)
    SEA_SHELL: ClassVar[Tuple[int, int, int]] = (255, 245, 238)
    MINT_CREAM: ClassVar[Tuple[int, int, int]] = (245, 255, 250)
    SLATE_GRAY: ClassVar[Tuple[int, int, int]] = (112, 128, 144)
    LIGHT_SLATE_GRAY: ClassVar[Tuple[int, int, int]] = (119, 136, 153)
    LIGHT_STEEL_BLUE: ClassVar[Tuple[int, int, int]] = (176, 196, 222)
    LAVENDER: ClassVar[Tuple[int, int, int]] = (230, 230, 250)
    FLORAL_WHITE: ClassVar[Tuple[int, int, int]] = (255, 250, 240)
    ALICE_BLUE: ClassVar[Tuple[int, int, int]] = (240, 248, 255)
    GHOST_WHITE: ClassVar[Tuple[int, int, int]] = (248, 248, 255)
    HONEYDEW: ClassVar[Tuple[int, int, int]] = (240, 255, 240)
    IVORY: ClassVar[Tuple[int, int, int]] = (255, 255, 240)
    AZURE: ClassVar[Tuple[int, int, int]] = (240, 255, 255)
    SNOW: ClassVar[Tuple[int, int, int]] = (255, 250, 250)
    BLACK: ClassVar[Tuple[int, int, int]] = (0, 0, 0)
    DIM_GRAY: ClassVar[Tuple[int, int, int]] = (105, 105, 105)
    GRAY: ClassVar[Tuple[int, int, int]] = (128, 128, 128)
    DARK_GRAY: ClassVar[Tuple[int, int, int]] = (169, 169, 169)
    SILVER: ClassVar[Tuple[int, int, int]] = (192, 192, 192)
    LIGHT_GRAY: ClassVar[Tuple[int, int, int]] = (211, 211, 211)
    GAINSBORO: ClassVar[Tuple[int, int, int]] = (220, 220, 220)
    WHITE_SMOKE: ClassVar[Tuple[int, int, int]] = (245, 245, 245)
    WHITE: ClassVar[Tuple[int, int, int]] = (255, 255, 255)

    @staticmethod
    def scale_to_01(color: Tuple[float, ...]) -> Tuple[float, ...]:
        """Scale color values from 0-255 to 0-1. Color can include alpha value.

        Args:
            color (Tuple[float, ...]): A tuple of length 3 or 4.

        Returns:
            Tuple[float, ...]: A scaped tuple.
        """
        return tuple(c / 255 for c in color)

    @staticmethod
    def alpha_extend(
        color: Tuple[int, int, int], alpha: int = 255
    ) -> Tuple[int, int, int, int]:
        """Extend a 3 value rgb tuple to include alpha color.

        Args:
            color (Tuple[int, int, int]): A rgb color value.
            alpha (int): The alpha value, 0-255. Defaults to 255.

        Returns:
            Tuple[int, int, int, int]: A rgba color value, 0-255.
        """
        return (*color, alpha)

    @staticmethod
    def alpha_extend_and_scale_to_01(
        color: Tuple[int, int, int], alpha: int = 255
    ) -> Tuple[float, ...]:
        """Performs both alpha extension and 0-1 scaling of a color.
        Use this method if you intent to do both to guarantee they
        are done in correct order.

        Args:
            color (Tuple[int, int, int]): A rgb color value.
            alpha (int, optional): The alpha value, 0-255. Defaults to 255.

        Returns:
            Tuple[float, float, float, float]: A rgba color value, 0-1.
        """
        return Color.scale_to_01(Color.alpha_extend(color, alpha))
