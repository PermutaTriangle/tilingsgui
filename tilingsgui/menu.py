"""Control stations.
"""


from typing import Iterable

import pyglet

from tilings import Tiling

from .events import CustomEvents, Observer
from .files import Images
from .geometry import Rectangle
from .graphics import Color, GeoDrawer
from .state import GuiState
from .utils import paste
from .widgets import Button, ButtonGrid, SelectionButton, TextBox, ToggleButton


class TopMenu(pyglet.event.EventDispatcher, Observer):
    """A menu that sits above the tiling plot.
    """

    _PADDING = 1
    _INITIAL_MESSAGE = " -- Basis here -- e.g. 1234_1324"
    _FONT_SIZE = 12
    _TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    _TEXT_BOX_COLOR = Color.DARK_GRAY
    _BACKGROUND_COLOR = Color.BLACK

    def __init__(
        self, x: int, y: int, w: int, h: int, dispatchers: Iterable[Observer]
    ) -> None:
        """Create the top menu.

        Args:
            x (int): The x coordinate of the SW corner of its surrounding rectangle.
            y (int): The y coordinate of the SW corner of its surrounding rectangle.
            w (int): The horizontal length of the surrounding rectangle.
            h (int): The vertical length of the surrounding rectangle.
            dispatchers (Iterable[Observer]): A collection of dispatchers that the menu
            should listen to.
        """
        Observer.__init__(self, dispatchers)
        self.rect: Rectangle = Rectangle(x, y, w, h)
        self.text_box: TextBox = TextBox(
            TopMenu._INITIAL_MESSAGE,
            TopMenu._FONT_SIZE,
            TopMenu._TEXT_COLOR,
            TopMenu._TEXT_BOX_COLOR,
        )
        self.position(w, h)

    def position(self, width: int, y: int) -> None:
        """Position the top bar, after a resize event.

        Args:
            width (int): The new width.
            y (int): The new vertical position.
        """
        self.rect.w = width
        self.rect.y = y
        self.text_box.position(
            self.rect.x + TopMenu._PADDING,
            self.rect.y + TopMenu._PADDING,
            self.rect.w - 2 * TopMenu._PADDING,
            self.rect.h - 2 * TopMenu._PADDING,
        )

    ##################
    # Event Handlers #
    ##################

    def on_draw(self):
        """Draw event handler.
        """
        GeoDrawer.draw_rectangle(
            self.rect.x,
            self.rect.y,
            self.rect.w,
            self.rect.h,
            TopMenu._BACKGROUND_COLOR,
        )
        self.text_box.draw()

    def on_key_press(self, symbol: int, _modifiers: int) -> bool:
        """Key pressed event handler.

        Args:
            symbol (int): The key pressed.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self.text_box.has_focus():
            if symbol == pyglet.window.key.ESCAPE:
                self.text_box.release_focus()
            elif symbol == pyglet.window.key.ENTER:
                self._dispatch_input_if_not_empty()
            return True
        return False

    def on_mouse_press(self, x: int, y: int, button: int, _modifiers: int) -> bool:
        """Mouse click event handler.

        Args:
            x (int): The x coordinate of the click.
            y (int): The y coordinate of the click.
            button (int): The mouse button that was clicked.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if not self.text_box.hit_test(x, y):
            if self.text_box.has_focus():
                self._dispatch_input_if_not_empty()
                return True
            return False
        if self.text_box.has_focus():
            if button == pyglet.window.mouse.RIGHT:
                self.text_box.add_text(paste())
        else:
            self.text_box.set_focus()
        return False

    def on_text(self, text: str) -> bool:
        """Text input event handler.

        Args:
            text (str): The newly written text.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self.text_box.has_focus():
            if text.isprintable():
                self.text_box.add_text(text)
            return True
        return False

    def on_text_motion(self, motion: int) -> bool:
        """Text motion event handler.

        Args:
            motion (int): The motion type.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self.text_box.has_focus():
            self.text_box.move_text(motion)
            return True
        return False

    ###################
    # Private helpers #
    ###################

    def _dispatch_input_if_not_empty(self):
        """Releases focus and reads the current input. If it is empty, do nothing.
        If it is a valid tiling json, dispatch a starting tiling decoded from it.
        Otherwise, use string to construct one with from_string.
        """
        self.text_box.release_focus()
        input_string = self.text_box.get_current_text()
        if not input_string:
            return
        if input_string[0] == "{" and input_string[-1] == "}":
            try:
                tiling = Tiling.from_json(input_string)
                self.dispatch_event(CustomEvents.ON_TILING_JSON_INPUT, tiling)
                return
            except ValueError:
                pass
        self.dispatch_event(CustomEvents.ON_BASIS_INPUT, input_string)


TopMenu.register_event_type(CustomEvents.ON_BASIS_INPUT)
TopMenu.register_event_type(CustomEvents.ON_TILING_JSON_INPUT)


class RightMenu(pyglet.event.EventDispatcher, Observer):
    _PADDING = 1
    _INITIAL_MESSAGE = "12"
    _FONT_SIZE = 12
    _TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    _TEXT_BOX_COLOR = Color.DARK_GRAY
    _BACKGROUND_COLOR = Color.BLACK

    def __init__(self, x, y, w, h, top, state: GuiState, dispatchers):
        Observer.__init__(self, dispatchers)
        self.rect: Rectangle = Rectangle(x, y, w, h)
        self.top: int = top
        self.state: GuiState = state
        self.text_box: TextBox = TextBox(
            RightMenu._INITIAL_MESSAGE,
            RightMenu._FONT_SIZE,
            RightMenu._TEXT_COLOR,
            RightMenu._TEXT_BOX_COLOR,
        )
        self.keyboard: ButtonGrid = ButtonGrid(8, 4)
        self._populate_keyboard()
        self.position(w, h)

    def position(self, width, height):
        self.rect.x = width
        self.rect.h = height
        self.text_box.position(
            self.rect.x + RightMenu._PADDING,
            self.rect.h - self.top + RightMenu._PADDING,
            self.rect.w - 2 * RightMenu._PADDING,
            self.top - 2 * RightMenu._PADDING,
        )
        self.keyboard.position(
            self.rect.x, self.rect.y, self.rect.w, self.rect.h - self.top
        )

    ##################
    # Event Handlers #
    ##################

    def on_draw(self):
        GeoDrawer.draw_rectangle(
            self.rect.x,
            self.rect.y,
            self.rect.w,
            self.rect.h,
            RightMenu._BACKGROUND_COLOR,
        )
        self.text_box.draw()
        self.keyboard.draw()

    def on_key_press(self, symbol, _modifiers):

        if self.text_box.has_focus():
            if symbol == pyglet.window.key.ESCAPE:
                self.text_box.release_focus()
            if symbol == pyglet.window.key.ENTER:
                self.text_box.release_focus()
                input_text = self.text_box.get_current_text()
                if input_text:
                    self.dispatch_event(CustomEvents.ON_PLACEMENT_INPUT, input_text)
            return True
        return False

    def on_mouse_press(self, x, y, button, _modifiers):
        if not self.text_box.hit_test(x, y):
            if self.text_box.has_focus():
                input_string = self.text_box.get_current_text()
                if input_string:
                    self.dispatch_event(CustomEvents.ON_PLACEMENT_INPUT, input_string)
                self.text_box.release_focus()
                return True
        else:
            if self.text_box.has_focus():
                if button == pyglet.window.mouse.RIGHT:
                    self.text_box.add_text(paste())
            else:
                self.text_box.set_focus()
            return False

        self.keyboard.click_check(x, y)

    def on_text(self, text):
        if self.text_box.has_focus():
            if text.isprintable():
                self.text_box.add_text(text)
            return True
        return False

    def on_text_motion(self, motion):
        if self.text_box.has_focus():
            self.text_box.move_text(motion)
            return True
        return False

    ###################
    # Private helpers #
    ###################

    def _populate_keyboard(self):
        self._add_selection_btns()
        self._add_btns()
        self._add_toggle_btns()

    def _add_selection_btns(self):
        positions = [
            (7, 0),
            (7, 1),
            (7, 2),
            (7, 3),
            (6, 0),
            (6, 1),
            (6, 2),
            (6, 3),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (3, 0),
        ]

        buttons = [
            SelectionButton(Images.ADD_POINT, selected=True),
            SelectionButton(Images.ADD_CUSOM),
            SelectionButton(Images.FACTOR),
            SelectionButton(Images.FACTOR_INT),
            SelectionButton(Images.PLACE_WEST),
            SelectionButton(Images.PLACE_EAST),
            SelectionButton(Images.PLACE_NORTH),
            SelectionButton(Images.PLACE_SOUTH),
            SelectionButton(Images.PPLACE_WEST),
            SelectionButton(Images.PPLACE_EAST),
            SelectionButton(Images.PPLACE_NORTH),
            SelectionButton(Images.PPLACE_SOUTH),
            SelectionButton(Images.FUSION_R),
            SelectionButton(Images.FUSION_C),
            SelectionButton(Images.FUSION_COM_R),
            SelectionButton(Images.FUSION_COM_C),
            SelectionButton(Images.MOVE),
        ]

        for pos, btn in zip(positions, buttons):
            self.keyboard.add_btn(*pos, btn)

        self.keyboard.add_selection_group(
            positions, on_click=self.state.set_mouse_click_action,
        )

    def _add_btns(self):
        self.keyboard.add_btn(
            3,
            2,
            Button(
                Images.UNDO, on_click=lambda: self.dispatch_event(CustomEvents.ON_UNDO)
            ),
        )
        self.keyboard.add_btn(
            3,
            3,
            Button(
                Images.REDO, on_click=lambda: self.dispatch_event(CustomEvents.ON_REDO)
            ),
        )
        self.keyboard.add_btn(
            2,
            0,
            Button(
                Images.EXPORT,
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_FETCH_TILING_FOR_EXPORT
                ),
            ),
        )
        self.keyboard.add_btn(
            2,
            1,
            Button(
                Images.SEQUENCE,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_PRINT_SEQUENCE),
            ),
        )
        self.keyboard.add_btn(
            2,
            2,
            Button(
                Images.STR,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_PRINT_TILING),
            ),
        )
        self.keyboard.add_btn(
            2,
            3,
            Button(
                Images.VERIFICATION,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_VERTIFICATION),
            ),
        )
        self.keyboard.add_btn(
            1,
            0,
            Button(
                Images.ROWCOLSEP,
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_ROW_COL_SEPERATION
                ),
            ),
        )
        self.keyboard.add_btn(
            1,
            1,
            Button(
                Images.OBSTR_TRANS,
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_OBSTRUCTION_TRANSIVITY
                ),
            ),
        )

    def _add_toggle_btns(self):
        self.keyboard.add_btn(
            1,
            3,
            ToggleButton(
                Images.HTC,
                on_click=self.state.toggle_highlight_touching_cell,
                toggled=self.state.highlight_touching_cell,
            ),
        )
        self.keyboard.add_btn(
            0,
            0,
            ToggleButton(
                Images.SHADING,
                on_click=self.state.toggle_shading,
                toggled=self.state.shading,
            ),
        )
        self.keyboard.add_btn(
            0,
            1,
            ToggleButton(
                Images.PRETTY,
                on_click=self.state.toggle_pretty_points,
                toggled=self.state.pretty_points,
            ),
        )
        self.keyboard.add_btn(
            0,
            2,
            ToggleButton(
                Images.SHOW_CROSS,
                on_click=self.state.toggle_show_crossing,
                toggled=self.state.show_crossing,
            ),
        )
        self.keyboard.add_btn(
            0,
            3,
            ToggleButton(
                Images.SHOW_LOCAL,
                on_click=self.state.toggle_show_localized,
                toggled=self.state.show_localized,
            ),
        )


RightMenu.register_event_type(CustomEvents.ON_PLACEMENT_INPUT)
RightMenu.register_event_type(CustomEvents.ON_FETCH_TILING_FOR_EXPORT)
RightMenu.register_event_type(CustomEvents.ON_UNDO)
RightMenu.register_event_type(CustomEvents.ON_REDO)
RightMenu.register_event_type(CustomEvents.ON_ROW_COL_SEPERATION)
RightMenu.register_event_type(CustomEvents.ON_OBSTRUCTION_TRANSIVITY)
RightMenu.register_event_type(CustomEvents.ON_PRINT_SEQUENCE)
RightMenu.register_event_type(CustomEvents.ON_PRINT_TILING)
RightMenu.register_event_type(CustomEvents.ON_VERTIFICATION)
