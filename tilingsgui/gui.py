

from typing import ClassVar, List, Tuple

import pyglet

from .graphics import Color
from .interface import Drawable, EventListener
from .tplot import TPlotManager


class TilingGui(pyglet.window.Window):

    TITLE: ClassVar[str] = 'Tilings GUI'

    MIN_WIDTH: ClassVar[int] = 300
    MIN_HEIGHT: ClassVar[int] = 300
    INITIAL_WIDTH: ClassVar[int] = 600
    INITIAL_HEIGHT: ClassVar[int] = 600

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

        tplot_man = TPlotManager(self.width, self.height)

        self.drawables: List[Drawable] = [
            tplot_man
        ]

        self.event_listeners: List[EventListener] = [
            tplot_man
        ]

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

        for drawable in self.drawables:
            drawable.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for event_listener in self.event_listeners:
            event_listener.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for event_listener in self.event_listeners:
            event_listener.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        for event_listener in self.event_listeners:
            event_listener.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        for event_listener in self.event_listeners:
            event_listener.on_mouse_drag(x, y, dx, dy, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        for event_listener in self.event_listeners:
            event_listener.on_key_press(symbol, modifiers)

    def on_resize(self, width, height):
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

        for event_listener in self.event_listeners:
            event_listener.on_resize(width, height)
