from typing import ClassVar, Tuple

import pyglet

from .files import History, PathManager
from .graphics import Color
from .menu import RightMenu, TopMenu
from .state import GuiState
from .tplot import TPlotManager


class Dispatcher(pyglet.event.EventDispatcher):
    def __init__(self):
        pass

    def fake_evt(self):
        self.dispatch_event("on_foo")


Dispatcher.register_event_type("on_foo")


class Observer:
    def __init__(self):
        pass

    def on_foo(self):
        print("IT IS HAPPENING!")


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

        self.dis = Dispatcher()
        self.obs = Observer()
        self.dis.push_handlers(self.obs)

        pyglet.resource.path = [PathManager.as_string(PathManager.get_png_abs_path())]

        self.state = GuiState()

        self.top_bar = TopMenu(
            0,
            self.height - TilingGui.TOP_BAR_HEIGHT,
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            TilingGui.TOP_BAR_HEIGHT,
            self.state,
        )
        self.right_bar = RightMenu(
            self.width - TilingGui.RIGHT_BAR_WIDTH,
            0,
            TilingGui.RIGHT_BAR_WIDTH,
            self.height,
            TilingGui.TOP_BAR_HEIGHT,
            self.state,
        )
        self.tplot_man = TPlotManager(self.width, self.height, self.state)

        self.delegate_handlers()

        self.history = History()

    def delegate_handlers(self):
        self.push_handlers(self.top_bar)
        self.push_handlers(self.right_bar)
        self.push_handlers(self.tplot_man)

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

    def on_close(self):
        super().on_close()
        self.clean_up()

    def clean_up(self):
        self.history.save()

    # The following should be delegated to subcomponents...
    #

    def on_mouse_press(self, x, y, button, modifiers):

        # TODO: consume some of these with custom evt handling and dispatchers...

        self.top_bar.XXXon_mouse_press(x, y, button, modifiers)
        if self.state.basis_input_read:
            self.tplot_man.add_from_string(self.state.basis_input_string)
            self.state.basis_input_read = False

        self.right_bar.XXXon_mouse_press(x, y, button, modifiers)
        if self.state.cell_input_read:
            self.tplot_man.set_custom_placement(self.state.cell_input_string)
            self.state.cell_input_read = False

        if self.state.export:
            tiling_json = self.tplot_man.get_current_tiling_json()
            self.history.add_tiling(tiling_json)
            self.state.export = False

        if self.state.undo:
            self.tplot_man.undo()
            self.state.undo = False

        if self.state.redo:
            self.tplot_man.redo()
            self.state.redo = False

        if self.state.row_col_seperation:
            self.tplot_man.row_col_seperation()
            self.state.row_col_seperation = False

        if self.state.obstruction_transivity:
            self.tplot_man.obstruction_transitivity()
            self.state.obstruction_transivity = False

        self.tplot_man.XXXon_mouse_press(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        self.dis.fake_evt()
        if self.state.basis_input_focus:
            self.top_bar.XXXon_key_press(symbol, modifiers)
            if self.state.basis_input_read:
                self.tplot_man.add_from_string(self.state.basis_input_string)
                self.state.basis_input_read = False
            return
        if self.state.cell_input_focus:
            self.right_bar.XXXon_key_press(symbol, modifiers)
            if self.state.cell_input_read:
                self.tplot_man.set_custom_placement(self.state.cell_input_string)
                self.state.cell_input_read = False
            return

        if symbol == pyglet.window.key.ESCAPE:
            self.clean_up()
            pyglet.app.exit()
