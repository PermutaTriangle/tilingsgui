"""Drawable objects
"""


from math import cos, pi, sin
from typing import ClassVar, List, Tuple

import pyglet

from .geometry import Point


class GeoDrawer:
    _VERTEX_MODE: ClassVar[str] = "v2f"
    _COLOR_MODE: ClassVar[str] = "c3B"

    @staticmethod
    def draw_line_segment(x1, y1, x2, y2, color):
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINE_STRIP,
            (GeoDrawer._VERTEX_MODE, [x1, y1, x2, y2]),
            (GeoDrawer._COLOR_MODE, color * 2),
        )

    @staticmethod
    def draw_circle(x, y, r, color, splits=30):
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
    def draw_point(point, size, color):
        GeoDrawer.draw_circle(point.x, point.y, size, color)

    @staticmethod
    def draw_filled_rectangle(x, y, w, h, color):
        vertices = [
            x,
            y,
            x,
            y + h,
            x + w,
            y,
            x + w,
            y + h,
        ]
        pyglet.graphics.draw(
            4,
            pyglet.gl.GL_TRIANGLE_STRIP,
            (GeoDrawer._VERTEX_MODE, vertices),
            (GeoDrawer._COLOR_MODE, color * 4),
        )

    @staticmethod
    def draw_point_path(pnt_path: List[Point], color, point_size):
        n = len(pnt_path)
        if n > 0:
            # TODO: Do in batch
            # Maybe always add to bash and support flushing it...
            if n > 1:
                vertices = [coord for pnt in pnt_path for coord in pnt]
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
    def scale_to_01(color: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Scale color values from 0-255 to 0-1. Color can include alpha value.

        Args:
            color (Tuple[float, ...]): A tuple of length 3 or 4.

        Returns:
            Tuple[float, ...]: A scaped tuple.
        """
        r, g, b = color
        return r / 255, g / 255, b / 255

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
    ) -> Tuple[float, float, float, float]:
        """Performs both alpha extension and 0-1 scaling of a color.
        Use this method if you intent to do both to guarantee they
        are done in correct order.

        Args:
            color (Tuple[int, int, int]): A rgb color value.
            alpha (int, optional): The alpha value, 0-255. Defaults to 255.

        Returns:
            Tuple[float, float, float, float]: A rgba color value, 0-1.
        """
        r, g, b = color
        return r / 255, g / 255, b / 255, alpha / 255
