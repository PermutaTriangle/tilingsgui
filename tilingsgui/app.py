from typing import ClassVar, Tuple

import pyglet

from .files import History, PathManager
from .graphics import Color
from .menu import RightMenu, TopMenu
from .state import GuiState
from .tplot import TPlotManager


class TilingGui(pyglet.window.Window):

    TITLE: ClassVar[str] = "Tilings GUI"
    MIN_WIDTH: ClassVar[int] = 500
    MIN_HEIGHT: ClassVar[int] = 400
    INITIAL_WIDTH: ClassVar[int] = 800
    INITIAL_HEIGHT: ClassVar[int] = 650
    RIGHT_BAR_WIDTH: ClassVar[int] = 200
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
            **kargs,
        )

        pyglet.resource.path = [PathManager.as_string(PathManager.get_png_abs_path())]

        self.state = GuiState()

        self.top_bar = TopMenu(
            0,
            self.height - TilingGui.TOP_BAR_HEIGHT,
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            TilingGui.TOP_BAR_HEIGHT,
            self.state,
            [self],
        )
        self.right_bar = RightMenu(
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            0,
            TilingGui.RIGHT_BAR_WIDTH,
            self.height,
            TilingGui.TOP_BAR_HEIGHT,
            self.state,
            [self],
        )
        self.tplot_man = TPlotManager(
            self.width, self.height, self.state, [self, self.top_bar, self.right_bar]
        )

        self.history = History([self, self.right_bar, self.tplot_man])

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

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.tplot_man.position(
            width - TilingGui.RIGHT_BAR_WIDTH, height - TilingGui.TOP_BAR_HEIGHT
        )
        self.top_bar.position(
            width - TilingGui.RIGHT_BAR_WIDTH, height - TilingGui.TOP_BAR_HEIGHT
        )
        self.right_bar.position(width - TilingGui.RIGHT_BAR_WIDTH, height)
