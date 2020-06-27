"""Drawable objects
"""


from math import cos, pi, sin
from typing import ClassVar, List, Tuple

import pyglet

from .geometry import Point

C3F = Tuple[float, float, float]
C4F = Tuple[float, float, float, float]
C3I = Tuple[int, int, int]
C4I = Tuple[int, int, int, int]


class GeoDrawer:
    """A static class container of drawing methods.
    """

    _VERTEX_MODE: ClassVar[str] = "v2f"
    _COLOR_MODE: ClassVar[str] = "c3B"

    @staticmethod
    def draw_line_segment(
        x1: float, y1: float, x2: float, y2: float, color: C3F
    ) -> None:
        """Draw a line segment.

        Args:
            x1 (float): Start x coordinate.
            y1 (float): Start y coordinate.
            x2 (float): End x coordinate.
            y2 (float): End y coordinate.
            color (Tuple[float, float, float]): RGB valued color.
        """
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINE_STRIP,
            (GeoDrawer._VERTEX_MODE, [x1, y1, x2, y2]),
            (GeoDrawer._COLOR_MODE, color * 2),
        )

    @staticmethod
    def draw_circle(x: float, y: float, r: float, color: C3F, splits: int = 30) -> None:
        """Draw a cricle.

        Args:
            x (float): The circle center's x coordinate.
            y (float): The circle center's y coordinate.
            r (float): The circle's radius.
            color (Tuple[float, float, float]): The fill color of the circle.
            splits (int, optional): How detailed the polygon emulating a circle should
            be. Higher values increase detail.
        """
        vertices = [x, y]
        for i in range(splits + 1):
            ang = 2 * pi * i / splits
            vertices.append(x + cos(ang) * r)
            vertices.append(y + sin(ang) * r)
        pyglet.graphics.draw(
            splits + 2,
            pyglet.gl.GL_TRIANGLE_FAN,
            (GeoDrawer._VERTEX_MODE, vertices),
            (GeoDrawer._COLOR_MODE, color * (splits + 2)),
        )

    @staticmethod
    def draw_point(point: Point, size: float, color: C3F) -> None:
        """Draw a point.

        Args:
            point (Point): The point object draw.
            size (float): The radius of the circle used to represent the point.
            color (Tuple[float, float, float]): The fill color.
        """
        GeoDrawer.draw_circle(point.x, point.y, size, color)

    @staticmethod
    def draw_rectangle(x: float, y: float, w: float, h: float, color: C3F) -> None:
        """Draw a rectangle.

        Args:
            x (float): South west corner's x coordinate.
            y (float): South west corner's y coordinate.
            w (float): Horizontal length.
            h (float): Vertical length.
            color (Tuple[float, float, float]): Fill color.
        """
        pyglet.graphics.draw(
            4,
            pyglet.gl.GL_TRIANGLE_STRIP,
            (GeoDrawer._VERTEX_MODE, [x, y, x, y + h, x + w, y, x + w, y + h]),
            (GeoDrawer._COLOR_MODE, color * 4),
        )

    @staticmethod
    def draw_point_path(pnt_path: List[Point], color: C3F, point_size: float) -> None:
        """Draw a list of point and a line segment between to adjacent points.

        Args:
            pnt_path (List[Point]): The list of points to draw in order.
            color (Tuple[float, float, float]): Color of line segments and point fills.
            point_size (float): Radius of the circle representing the points.
        """
        n = len(pnt_path)
        if n > 0:
            if n > 1:
                vertices = [coord for pnt in pnt_path for coord in pnt.coords()]
                pyglet.graphics.draw(
                    n,
                    pyglet.gl.GL_LINE_STRIP,
                    (GeoDrawer._VERTEX_MODE, vertices),
                    (GeoDrawer._COLOR_MODE, color * n),
                )
            for pnt in pnt_path:
                GeoDrawer.draw_point(pnt, point_size, color)


class Color:
    """A collection of color constants.
    """

    # Scraped with bs4 from https://www.rapidtables.com/web/color/RGB_Color.html.

    MAROON: ClassVar[C3I] = (128, 0, 0)
    DARK_RED: ClassVar[C3I] = (139, 0, 0)
    BROWN: ClassVar[C3I] = (165, 42, 42)
    FIREBRICK: ClassVar[C3I] = (178, 34, 34)
    CRIMSON: ClassVar[C3I] = (220, 20, 60)
    RED: ClassVar[C3I] = (255, 0, 0)
    TOMATO: ClassVar[C3I] = (255, 99, 71)
    CORAL: ClassVar[C3I] = (255, 127, 80)
    INDIAN_RED: ClassVar[C3I] = (205, 92, 92)
    LIGHT_CORAL: ClassVar[C3I] = (240, 128, 128)
    DARK_SALMON: ClassVar[C3I] = (233, 150, 122)
    SALMON: ClassVar[C3I] = (250, 128, 114)
    LIGHT_SALMON: ClassVar[C3I] = (255, 160, 122)
    ORANGE_RED: ClassVar[C3I] = (255, 69, 0)
    DARK_ORANGE: ClassVar[C3I] = (255, 140, 0)
    ORANGE: ClassVar[C3I] = (255, 165, 0)
    GOLD: ClassVar[C3I] = (255, 215, 0)
    DARK_GOLDEN_ROD: ClassVar[C3I] = (184, 134, 11)
    GOLDEN_ROD: ClassVar[C3I] = (218, 165, 32)
    PALE_GOLDEN_ROD: ClassVar[C3I] = (238, 232, 170)
    DARK_KHAKI: ClassVar[C3I] = (189, 183, 107)
    KHAKI: ClassVar[C3I] = (240, 230, 140)
    OLIVE: ClassVar[C3I] = (128, 128, 0)
    YELLOW: ClassVar[C3I] = (255, 255, 0)
    YELLOW_GREEN: ClassVar[C3I] = (154, 205, 50)
    DARK_OLIVE_GREEN: ClassVar[C3I] = (85, 107, 47)
    OLIVE_DRAB: ClassVar[C3I] = (107, 142, 35)
    LAWN_GREEN: ClassVar[C3I] = (124, 252, 0)
    CHART_REUSE: ClassVar[C3I] = (127, 255, 0)
    GREEN_YELLOW: ClassVar[C3I] = (173, 255, 47)
    DARK_GREEN: ClassVar[C3I] = (0, 100, 0)
    GREEN: ClassVar[C3I] = (0, 128, 0)
    FOREST_GREEN: ClassVar[C3I] = (34, 139, 34)
    LIME: ClassVar[C3I] = (0, 255, 0)
    LIME_GREEN: ClassVar[C3I] = (50, 205, 50)
    LIGHT_GREEN: ClassVar[C3I] = (144, 238, 144)
    PALE_GREEN: ClassVar[C3I] = (152, 251, 152)
    DARK_SEA_GREEN: ClassVar[C3I] = (143, 188, 143)
    MEDIUM_SPRING_GREEN: ClassVar[C3I] = (0, 250, 154)
    SPRING_GREEN: ClassVar[C3I] = (0, 255, 127)
    SEA_GREEN: ClassVar[C3I] = (46, 139, 87)
    MEDIUM_AQUA_MARINE: ClassVar[C3I] = (102, 205, 170)
    MEDIUM_SEA_GREEN: ClassVar[C3I] = (60, 179, 113)
    LIGHT_SEA_GREEN: ClassVar[C3I] = (32, 178, 170)
    DARK_SLATE_GRAY: ClassVar[C3I] = (47, 79, 79)
    TEAL: ClassVar[C3I] = (0, 128, 128)
    DARK_CYAN: ClassVar[C3I] = (0, 139, 139)
    AQUA: ClassVar[C3I] = (0, 255, 255)
    CYAN: ClassVar[C3I] = (0, 255, 255)
    LIGHT_CYAN: ClassVar[C3I] = (224, 255, 255)
    DARK_TURQUOISE: ClassVar[C3I] = (0, 206, 209)
    TURQUOISE: ClassVar[C3I] = (64, 224, 208)
    MEDIUM_TURQUOISE: ClassVar[C3I] = (72, 209, 204)
    PALE_TURQUOISE: ClassVar[C3I] = (175, 238, 238)
    AQUA_MARINE: ClassVar[C3I] = (127, 255, 212)
    POWDER_BLUE: ClassVar[C3I] = (176, 224, 230)
    CADET_BLUE: ClassVar[C3I] = (95, 158, 160)
    STEEL_BLUE: ClassVar[C3I] = (70, 130, 180)
    CORN_FLOWER_BLUE: ClassVar[C3I] = (100, 149, 237)
    DEEP_SKY_BLUE: ClassVar[C3I] = (0, 191, 255)
    DODGER_BLUE: ClassVar[C3I] = (30, 144, 255)
    LIGHT_BLUE: ClassVar[C3I] = (173, 216, 230)
    SKY_BLUE: ClassVar[C3I] = (135, 206, 235)
    LIGHT_SKY_BLUE: ClassVar[C3I] = (135, 206, 250)
    MIDNIGHT_BLUE: ClassVar[C3I] = (25, 25, 112)
    NAVY: ClassVar[C3I] = (0, 0, 128)
    DARK_BLUE: ClassVar[C3I] = (0, 0, 139)
    MEDIUM_BLUE: ClassVar[C3I] = (0, 0, 205)
    BLUE: ClassVar[C3I] = (0, 0, 255)
    ROYAL_BLUE: ClassVar[C3I] = (65, 105, 225)
    BLUE_VIOLET: ClassVar[C3I] = (138, 43, 226)
    INDIGO: ClassVar[C3I] = (75, 0, 130)
    DARK_SLATE_BLUE: ClassVar[C3I] = (72, 61, 139)
    SLATE_BLUE: ClassVar[C3I] = (106, 90, 205)
    MEDIUM_SLATE_BLUE: ClassVar[C3I] = (123, 104, 238)
    MEDIUM_PURPLE: ClassVar[C3I] = (147, 112, 219)
    DARK_MAGENTA: ClassVar[C3I] = (139, 0, 139)
    DARK_VIOLET: ClassVar[C3I] = (148, 0, 211)
    DARK_ORCHID: ClassVar[C3I] = (153, 50, 204)
    MEDIUM_ORCHID: ClassVar[C3I] = (186, 85, 211)
    PURPLE: ClassVar[C3I] = (128, 0, 128)
    THISTLE: ClassVar[C3I] = (216, 191, 216)
    PLUM: ClassVar[C3I] = (221, 160, 221)
    VIOLET: ClassVar[C3I] = (238, 130, 238)
    MAGENTA: ClassVar[C3I] = (255, 0, 255)
    ORCHID: ClassVar[C3I] = (218, 112, 214)
    MEDIUM_VIOLET_RED: ClassVar[C3I] = (199, 21, 133)
    PALE_VIOLET_RED: ClassVar[C3I] = (219, 112, 147)
    DEEP_PINK: ClassVar[C3I] = (255, 20, 147)
    HOT_PINK: ClassVar[C3I] = (255, 105, 180)
    LIGHT_PINK: ClassVar[C3I] = (255, 182, 193)
    PINK: ClassVar[C3I] = (255, 192, 203)
    ANTIQUE_WHITE: ClassVar[C3I] = (250, 235, 215)
    BEIGE: ClassVar[C3I] = (245, 245, 220)
    BISQUE: ClassVar[C3I] = (255, 228, 196)
    BLANCHED_ALMOND: ClassVar[C3I] = (255, 235, 205)
    WHEAT: ClassVar[C3I] = (245, 222, 179)
    CORN_SILK: ClassVar[C3I] = (255, 248, 220)
    LEMON_CHIFFON: ClassVar[C3I] = (255, 250, 205)
    LIGHT_GOLDEN_ROD_YELLOW: ClassVar[C3I] = (250, 250, 210)
    LIGHT_YELLOW: ClassVar[C3I] = (255, 255, 224)
    SADDLE_BROWN: ClassVar[C3I] = (139, 69, 19)
    SIENNA: ClassVar[C3I] = (160, 82, 45)
    CHOCOLATE: ClassVar[C3I] = (210, 105, 30)
    PERU: ClassVar[C3I] = (205, 133, 63)
    SANDY_BROWN: ClassVar[C3I] = (244, 164, 96)
    BURLY_WOOD: ClassVar[C3I] = (222, 184, 135)
    TAN: ClassVar[C3I] = (210, 180, 140)
    ROSY_BROWN: ClassVar[C3I] = (188, 143, 143)
    MOCCASIN: ClassVar[C3I] = (255, 228, 181)
    NAVAJO_WHITE: ClassVar[C3I] = (255, 222, 173)
    PEACH_PUFF: ClassVar[C3I] = (255, 218, 185)
    MISTY_ROSE: ClassVar[C3I] = (255, 228, 225)
    LAVENDER_BLUSH: ClassVar[C3I] = (255, 240, 245)
    LINEN: ClassVar[C3I] = (250, 240, 230)
    OLD_LACE: ClassVar[C3I] = (253, 245, 230)
    PAPAYA_WHIP: ClassVar[C3I] = (255, 239, 213)
    SEA_SHELL: ClassVar[C3I] = (255, 245, 238)
    MINT_CREAM: ClassVar[C3I] = (245, 255, 250)
    SLATE_GRAY: ClassVar[C3I] = (112, 128, 144)
    LIGHT_SLATE_GRAY: ClassVar[C3I] = (119, 136, 153)
    LIGHT_STEEL_BLUE: ClassVar[C3I] = (176, 196, 222)
    LAVENDER: ClassVar[C3I] = (230, 230, 250)
    FLORAL_WHITE: ClassVar[C3I] = (255, 250, 240)
    ALICE_BLUE: ClassVar[C3I] = (240, 248, 255)
    GHOST_WHITE: ClassVar[C3I] = (248, 248, 255)
    HONEYDEW: ClassVar[C3I] = (240, 255, 240)
    IVORY: ClassVar[C3I] = (255, 255, 240)
    AZURE: ClassVar[C3I] = (240, 255, 255)
    SNOW: ClassVar[C3I] = (255, 250, 250)
    BLACK: ClassVar[C3I] = (0, 0, 0)
    DIM_GRAY: ClassVar[C3I] = (105, 105, 105)
    GRAY: ClassVar[C3I] = (128, 128, 128)
    DARK_GRAY: ClassVar[C3I] = (169, 169, 169)
    SILVER: ClassVar[C3I] = (192, 192, 192)
    LIGHT_GRAY: ClassVar[C3I] = (211, 211, 211)
    GAINSBORO: ClassVar[C3I] = (220, 220, 220)
    WHITE_SMOKE: ClassVar[C3I] = (245, 245, 245)
    WHITE: ClassVar[C3I] = (255, 255, 255)

    @staticmethod
    def scale_to_01(color: C3I) -> C3F:
        """Scale color values from 0-255 to 0-1. Color can include alpha value.

        Args:
            color (Tuple[int, int, int]): A tuple of length 3.

        Returns:
            Tuple[float, float, float]: A scaled tuple.
        """
        r, g, b = color
        return r / 255, g / 255, b / 255

    @staticmethod
    def alpha_extend(color: C3I, alpha: int = 255) -> C4I:
        """Extend a 3 value rgb tuple to include alpha color.

        Args:
            color (Tuple[int, int, int]): A rgb color value.
            alpha (int): The alpha value, 0-255. Defaults to 255.

        Returns:
            Tuple[int, int, int, int]: A rgba color value, 0-255.
        """
        return (*color, alpha)

    @staticmethod
    def alpha_extend_and_scale_to_01(color: C3I, alpha: int = 255) -> C4F:
        """Performs both alpha extension and 0-1 scaling of a color.
        Use this method if you intent to do both to guarantee they
        are done in correct order.

        Args:
            color (Tuple[int, int, int]): A rgb color value.
            alpha (int, optional): The alpha value, 0-255. Defaults to 255.

        Returns:
            Tuple[int, int, int, int]: A rgba color value, 0-1.
        """
        r, g, b = color
        return r / 255, g / 255, b / 255, alpha / 255
