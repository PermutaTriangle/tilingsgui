"""A module containing the app itself. This should be
the only module needed to import by the script that
runs it.
"""

# pylint: disable=abstract-method

import sys
from typing import ClassVar, Literal, Tuple

import pyglet

# PyPy compatibility on macOS
#
# PyPy is not supported on macOS due to fundamental incompatibilities between PyPy's
# ctypes implementation and macOS GUI frameworks. This issue affects ALL major Python
# GUI libraries, not just pyglet.
#
# Investigation conducted (Oct 2025) found the following:
#
# 1. pyglet 2.0:
#    - Fails with IndexError/AttributeError in PyPy's ctypes when interfacing with
#      Cocoa/Objective-C bridge
#    - pyglet.options like shadow_window=False and osx_alt_loop=True do not help
#
# 2. Tkinter:
#    - Imports successfully but hangs when creating windows
#    - PyPy's bundled Tk requires manual mainloop() calls, breaking event-driven design
#    - Tested with PyPy 7.3.20 (Python 3.11.13) - same issues
#
# 3. PySide6 (Qt):
#    - Officially supports PyPy 3.8+ but no pre-built PyPy wheels available for macOS
#    - Would require building from source
#
# 4. wxPython:
#    - Community reports indicate it does not work with PyPy
#
# Root cause: PyPy's ctypes has subtle differences from CPython in callback and object
# reference handling, which breaks all macOS GUI frameworks that use ctypes to interface
# with Cocoa/Objective-C.
#
# Note: PyPy may work on Linux (X11) or Windows (Win32), as the issue is specific to
# macOS's Cocoa backend.
if sys.platform == "darwin" and sys.implementation.name == "pypy":
    print("Error: PyPy is not supported on macOS.")
    print("Reason: PyPy's ctypes is incompatible with macOS GUI frameworks (Cocoa).")
    print("Please use CPython on macOS, or try PyPy on Linux/Windows.")
    sys.exit(1)

# pylint: disable=wrong-import-position
from .files import History, PathManager
from .graphics import Color
from .menu import RightMenu, TopMenu
from .state import GuiState
from .tplot import TPlotManager


class TilingGui(pyglet.window.Window):
    """The TilingsGui application."""

    _TITLE: ClassVar[str] = "Tilings GUI"
    _MIN_WIDTH: ClassVar[int] = 500
    _MIN_HEIGHT: ClassVar[int] = 400
    _INITIAL_WIDTH: ClassVar[int] = 1600
    _INITIAL_HEIGHT: ClassVar[int] = 1200
    _RIGHT_BAR_WIDTH: ClassVar[int] = 400
    _TOP_BAR_HEIGHT: ClassVar[int] = 50
    _CLEAR_COLOR: ClassVar[Tuple[float, float, float, float]] = (
        Color.alpha_extend_and_scale_to_01(Color.WHITE)
    )

    def __init__(self, init_tiling: str, *args, **kargs) -> None:
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
            self.width, self.height, self._state, init_tiling=init_tiling
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
        """Start the app."""
        self._initial_config()
        pyglet.app.run()

    def _initial_config(self) -> None:
        """Configuration done before starting."""

        # Center the window within the os.
        screen = pyglet.display.Display().get_default_screen()  # type: ignore
        self.set_location(
            (screen.width - self.width) // 2, (screen.height - self.height) // 2
        )

        # Limit how small the window may be.
        self.set_minimum_size(TilingGui._MIN_WIDTH, TilingGui._MIN_HEIGHT)

        # Handle clearing the canvas on each draw.
        pyglet.gl.glClearColor(*TilingGui._CLEAR_COLOR)
        self.push_handlers(on_draw=self.clear)  # pylint: disable=unreachable

    def on_resize(self, width: int, height: int) -> Literal[True]:
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
