

from typing import ClassVar, Tuple

import pyglet
from tilingsgui.graphics import Color
from tilingsgui.menu import RightMenu, TopMenu
from tilingsgui.tplot import TPlotManager


class TilingGui(pyglet.window.Window):

    TITLE: ClassVar[str] = 'Tilings GUI'

    MIN_WIDTH: ClassVar[int] = 400
    MIN_HEIGHT: ClassVar[int] = 400
    INITIAL_WIDTH: ClassVar[int] = 700
    INITIAL_HEIGHT: ClassVar[int] = 650
    RIGHT_BAR_WIDTH: ClassVar[int] = 100
    TOP_BAR_HEIGHT: ClassVar[int] = 24

    CLEAR_COLOR: ClassVar[Tuple[float, ...]] = Color.alpha_extend_and_scale_to_01(
        Color.WHITE
    )

    def __init__(self, *args, **kargs) -> None:
        super().__init__(
            TilingGui.INITIAL_WIDTH,
            TilingGui.INITIAL_HEIGHT,
            TilingGui.TITLE,
            *args,
            **kargs
        )
        self.tplot_man = TPlotManager(self.width, self.height)
        self.top_bar = TopMenu(
            0,
            self.height - TilingGui.TOP_BAR_HEIGHT,
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            TilingGui.TOP_BAR_HEIGHT
        )
        self.right_bar = RightMenu(
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            0,
            TilingGui.RIGHT_BAR_WIDTH,
            self.height
        )

    def start(self) -> None:
        self._initial_config()
        pyglet.app.run()

    def _initial_config(self):
        screen = pyglet.canvas.Display().get_default_screen()
        self.set_location(
            (screen.width - self.width) // 2, (screen.height - self.height) // 2
        )
        self.set_minimum_size(TilingGui.MIN_WIDTH, TilingGui.MIN_HEIGHT)
        pyglet.gl.glClearColor(*TilingGui.CLEAR_COLOR)

    def on_draw(self):
        self.clear()

        self.tplot_man.draw()
        self.top_bar.draw()
        self.right_bar.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.top_bar.on_mouse_press(x, y, button, modifiers)

        if self.top_bar.string_to_process:
            self.tplot_man.add_from_string(self.top_bar.string_to_process.pop())

    def on_mouse_motion(self, x, y, dx, dy):
        self.tplot_man.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        if self.top_bar.has_focus():
            self.top_bar.on_key_press(symbol, modifiers)
            if self.top_bar.string_to_process:
                self.tplot_man.add_from_string(self.top_bar.string_to_process.pop())
            return

        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def on_resize(self, width, height):
        super().on_resize(width, height)

        self.tplot_man.on_resize(
            width - TilingGui.RIGHT_BAR_WIDTH,
            height - TilingGui.TOP_BAR_HEIGHT
        )
        self.top_bar.on_resize(
            width - TilingGui.RIGHT_BAR_WIDTH,
            height - TilingGui.TOP_BAR_HEIGHT
        )
        self.right_bar.on_resize(width - TilingGui.RIGHT_BAR_WIDTH, height)

    def on_text(self, text):
        self.top_bar.on_text(text)

    def on_text_motion(self, motion):
        self.top_bar.on_text_motion(motion)
