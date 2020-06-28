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

    _TITLE: ClassVar[str] = "Tilings GUI"
    _MIN_WIDTH: ClassVar[int] = 500
    _MIN_HEIGHT: ClassVar[int] = 400
    _INITIAL_WIDTH: ClassVar[int] = 800
    _INITIAL_HEIGHT: ClassVar[int] = 650
    _RIGHT_BAR_WIDTH: ClassVar[int] = 200
    _TOP_BAR_HEIGHT: ClassVar[int] = 24
    _CLEAR_COLOR: ClassVar[Tuple[float, float, float, float]] = (
        Color.alpha_extend_and_scale_to_01(Color.WHITE)
    )

    def __init__(self, *args, **kargs) -> None:
        """Instantiate the parent window class and create all
        sub components and systems for the app.
        """
        super().__init__(
            TilingGui._INITIAL_WIDTH,
            TilingGui._INITIAL_HEIGHT,
            TilingGui._TITLE,
            *args,
            **kargs,
        )

        # Create a list of all directories pyglet should search for resources
        pyglet.resource.path = [PathManager.as_string(PathManager.get_png_abs_path())]

        # The current state with initial values.
        self._state: GuiState = GuiState()

        # The bar above the tiling plot.
        self._top_bar: TopMenu = TopMenu(
            0,
            self.height - TilingGui._TOP_BAR_HEIGHT,
            self.width - TilingGui._RIGHT_BAR_WIDTH,
            TilingGui._TOP_BAR_HEIGHT,
        )

        # The bar to the right of the tiling plot.
        self._right_bar: RightMenu = RightMenu(
            self.width - TilingGui._RIGHT_BAR_WIDTH,
            0,
            TilingGui._RIGHT_BAR_WIDTH,
            self.height,
            TilingGui._TOP_BAR_HEIGHT,
            self._state,
        )

        # The tiling plot.
        self._tplot_man: TPlotManager = TPlotManager(
            self.width, self.height, self._state
        )

        # export data handler.
        self._history: History = History()

        # Add dispatchers. Order matters if events are consumed. Those that add
        # a dispatcher later will receive callbacks before.
        self._tplot_man.add_dispatchers([self, self._top_bar, self._right_bar])
        self._history.add_dispatchers([self, self._right_bar, self._tplot_man])
        self._top_bar.add_dispatcher(self)
        self._right_bar.add_dispatcher(self)

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
        self.set_minimum_size(TilingGui._MIN_WIDTH, TilingGui._MIN_HEIGHT)

        # Handle clearing the canvas on each draw.
        pyglet.gl.glClearColor(*TilingGui._CLEAR_COLOR)
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
        self._tplot_man.position(
            width - TilingGui._RIGHT_BAR_WIDTH, height - TilingGui._TOP_BAR_HEIGHT
        )
        self._top_bar.position(
            width - TilingGui._RIGHT_BAR_WIDTH, height - TilingGui._TOP_BAR_HEIGHT
        )
        self._right_bar.position(width - TilingGui._RIGHT_BAR_WIDTH, height)

        # on_resize is not handle anywhere else, so we can stop looking for handlers.
        return True
