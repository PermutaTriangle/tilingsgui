"""[TODO]
"""

import pyglet
from . import colors


class TilingGui(pyglet.window.Window):
    """[summary]
    """

    TITLE = "Tilings GUI"

    MIN_WIDTH = 300
    MIN_HEIGHT = 300
    INITIAL_WIDTH = 600
    INITIAL_HEIGHT = 600

    CLEAR_COLOR = colors.alpha_extend_and_scale_to_01(colors.WHITE)

    @staticmethod
    def start() -> None:
        """[summary]
        """
        pyglet.app.run()

    def __init__(self, *args, **kargs) -> None:
        """[summary]
        """
        super().__init__(
            TilingGui.INITIAL_WIDTH,
            TilingGui.INITIAL_HEIGHT,
            TilingGui.TITLE,
            *args,
            **kargs
        )

    def initial_configure(self) -> None:
        """[summary]
        """
        screen = pyglet.canvas.Display().get_default_screen()
        self.set_location(
            (screen.width - self.width) // 2, (screen.height - self.height) // 2
        )
        self.set_minimum_size(TilingGui.MIN_WIDTH, TilingGui.MIN_HEIGHT)
        pyglet.gl.glClearColor(*TilingGui.CLEAR_COLOR)

    def on_draw(self):
        self.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_resize(self, width, height):
        super().on_resize(width, height)
        print(width, height)
