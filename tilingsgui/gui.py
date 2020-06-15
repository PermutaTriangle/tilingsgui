

from typing import ClassVar, Tuple

import pyglet
import pyperclip

from tilingsgui.graphics import Color
from tilingsgui.tplot import TPlotManager
from tilingsgui.widgets import TextBox


class TilingGui(pyglet.window.Window):

    TITLE: ClassVar[str] = 'Tilings GUI'

    MIN_WIDTH: ClassVar[int] = 400
    MIN_HEIGHT: ClassVar[int] = 350
    INITIAL_WIDTH: ClassVar[int] = 700
    INITIAL_HEIGHT: ClassVar[int] = 650
    RIGHT_BAR_WIDTH: ClassVar[int] = 100
    TOP_BAR_HEIGHT: ClassVar[int] = 50

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

        self.tb = TextBox('', 0, 625, 400)

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

        self.tb.draw()
        self.tplot_man.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.tplot_man.on_mouse_press(x, y, button, modifiers)
        if self.tb.hit_test(x, y):
            if button == pyglet.window.mouse.LEFT:
                self.tb.set_focus()
            elif button == pyglet.window.mouse.RIGHT:
                self.tb.set_focus(with_text=pyperclip.paste())

    def on_mouse_motion(self, x, y, dx, dy):
        self.tplot_man.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        self.tplot_man.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.tplot_man.on_mouse_drag(x, y, dx, dy, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        self.tplot_man.on_key_press(symbol, modifiers)

    def on_resize(self, width, height):
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

        self.tplot_man.on_resize(width - TilingGui.RIGHT_BAR_WIDTH, height - TilingGui.TOP_BAR_HEIGHT)

    def on_text(self, text):
        if self.tb.focused:
            self.tb.on_text(text)

    def on_text_motion(self, motion):
        if self.tb.focused:
            self.tb.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.tb.focused:
            self.tb.on_text_motion_select(motion)
