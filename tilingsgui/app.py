"""A module containing the app itself. This should be
the only module needed to import by the script that
runs it.
"""

from typing import ClassVar, Tuple

import pyglet

from .files import History, PathManager
from .graphics import Color
from .menu import RightMenu, TopMenu
from .state import GuiState
from .tplot import TPlotManager


class TilingGui(pyglet.window.Window):
    """The TilingsGui application.
    """

    TITLE: ClassVar[str] = "Tilings GUI"
    MIN_WIDTH: ClassVar[int] = 500
    MIN_HEIGHT: ClassVar[int] = 400
    INITIAL_WIDTH: ClassVar[int] = 800
    INITIAL_HEIGHT: ClassVar[int] = 650
    RIGHT_BAR_WIDTH: ClassVar[int] = 200
    TOP_BAR_HEIGHT: ClassVar[int] = 24
    CLEAR_COLOR: ClassVar[Tuple[float, float, float, float]] = (
        Color.alpha_extend_and_scale_to_01(Color.WHITE)
    )

    def __init__(self, *args, **kargs) -> None:
        """Instantiate the parent window class and create all
        sub components and systems for the app.
        """
        super().__init__(
            TilingGui.INITIAL_WIDTH,
            TilingGui.INITIAL_HEIGHT,
            TilingGui.TITLE,
            *args,
            **kargs,
        )

        # Create a list of all directories pyglet should search for resources
        pyglet.resource.path = [PathManager.as_string(PathManager.get_png_abs_path())]

        # The current state with initial values.
        self.state = GuiState()

        # The bar above the tiling plot.
        self.top_bar = TopMenu(
            0,
            self.height - TilingGui.TOP_BAR_HEIGHT,
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            TilingGui.TOP_BAR_HEIGHT,
            [self],
        )

        # The bar to the right of the tiling plot.
        self.right_bar = RightMenu(
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            0,
            TilingGui.RIGHT_BAR_WIDTH,
            self.height,
            TilingGui.TOP_BAR_HEIGHT,
            self.state,
            [self],
        )

        # The tiling plot.
        self.tplot_man = TPlotManager(
            self.width, self.height, self.state, [self, self.top_bar, self.right_bar]
        )

        # export data handler.
        self.history = History([self, self.right_bar, self.tplot_man])

    def start(self) -> None:
        """Start the app.
        """
        self._initial_config()
        pyglet.app.run()

    def _initial_config(self) -> None:
        """Configuration done before starting.
        """

        # Center the window within the os.
        screen = pyglet.canvas.Display().get_default_screen()
        self.set_location(
            (screen.width - self.width) // 2, (screen.height - self.height) // 2
        )

        # Limit how small the window may be.
        self.set_minimum_size(TilingGui.MIN_WIDTH, TilingGui.MIN_HEIGHT)

        # Handle clearing the canvas on each draw.
        pyglet.gl.glClearColor(*TilingGui.CLEAR_COLOR)
        self.push_handlers(on_draw=self.clear)

    def on_resize(self, width: int, height: int) -> bool:
        """Event handler for the window resize event.

        Args:
            width (int): The window's width in pixels.
            height (int): The window's height in pixels.

        Returns:
            bool: True, as we do not wish to delegate this even further.
        """
        # Set up orthogonal projection
        super().on_resize(width, height)

        # Re-position subcomponents.
        self.tplot_man.position(
            width - TilingGui.RIGHT_BAR_WIDTH, height - TilingGui.TOP_BAR_HEIGHT
        )
        self.top_bar.position(
            width - TilingGui.RIGHT_BAR_WIDTH, height - TilingGui.TOP_BAR_HEIGHT
        )
        self.right_bar.position(width - TilingGui.RIGHT_BAR_WIDTH, height)

        # on_resize is not handle anywhere else, so we can stop looking for handlers.
        return True
