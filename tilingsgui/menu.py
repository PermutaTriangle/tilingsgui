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
    """A menu that sits above the tiling plot."""

    _PADDING = 1
    _INITIAL_MESSAGE = " -- Basis here -- e.g. 1234_1324"
    _FONT_SIZE = 12
    _TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    _TEXT_BOX_COLOR = Color.DARK_GRAY
    _BACKGROUND_COLOR = Color.BLACK
    _V_BTN = 118
    _CTRL_MODIFIER = 18

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        dispatchers: Iterable[pyglet.event.EventDispatcher] = (),
    ) -> None:
        """Create the top menu.

        Args:
            x (int): The x coordinate of the SW corner of its surrounding rectangle.
            y (int): The y coordinate of the SW corner of its surrounding rectangle.
            w (int): The horizontal length of the surrounding rectangle.
            h (int): The vertical length of the surrounding rectangle.
            dispatchers (Iterable[Observer]): A collection of dispatchers that the menu
            should listen to. Defaults to an empty tuple.
        """
        Observer.__init__(self, dispatchers)
        self._rect: Rectangle = Rectangle(x, y, w, h)
        self._text_box: TextBox = TextBox(
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
        self._rect.w = width
        self._rect.y = y
        self._text_box.position(
            self._rect.x + TopMenu._PADDING,
            self._rect.y + TopMenu._PADDING,
            self._rect.w - 2 * TopMenu._PADDING,
            self._rect.h - 2 * TopMenu._PADDING,
        )

    ##################
    # Event Handlers #
    ##################

    def on_draw(self):
        """Draw event handler."""
        GeoDrawer.draw_rectangle(
            self._rect.x,
            self._rect.y,
            self._rect.w,
            self._rect.h,
            TopMenu._BACKGROUND_COLOR,
        )
        self._text_box.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool:
        """Key pressed event handler.

        Args:
            symbol (int): The key pressed.
            modifiers (int): If combinded with modifiers (e.g. ctrl).

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self._text_box.has_focus():
            if symbol == TopMenu._V_BTN and modifiers == TopMenu._CTRL_MODIFIER:
                self._text_box.add_text(paste())
                return True
            if symbol == pyglet.window.key.ESCAPE:
                self._text_box.release_focus()
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
        if not self._text_box.hit_test(x, y):
            if self._text_box.has_focus():
                self._dispatch_input_if_not_empty()
                return True
            return False
        if self._text_box.has_focus():
            if button == pyglet.window.mouse.RIGHT:
                self._text_box.add_text(paste())
        else:
            self._text_box.set_focus()
        return False

    def on_text(self, text: str) -> bool:
        """Text input event handler. If text box does not have focus, we ignore it.
        All non-printable characters are also ignored.

        Args:
            text (str): The newly written text.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self._text_box.has_focus():
            if text.isprintable():
                self._text_box.add_text(text)
            return True
        return False

    def on_text_motion(self, motion: int) -> bool:
        """Text motion event handler.

        Args:
            motion (int): The motion type.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self._text_box.has_focus():
            self._text_box.move_text(motion)
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
        self._text_box.release_focus()
        input_string = self._text_box.get_current_text()
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
    """A menu that sits to the right of the tiling plot."""

    _PADDING = 1
    _INITIAL_MESSAGE = "12"
    _FONT_SIZE = 12
    _TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    _TEXT_BOX_COLOR = Color.DARK_GRAY
    _BACKGROUND_COLOR = Color.BLACK

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        top: int,
        state: GuiState,
        dispatchers: Iterable[pyglet.event.EventDispatcher] = (),
    ) -> None:
        """Create a right menu instance.

        Args:
            x (int): The x coordinate of the SW corner of its surrounding rectangle.
            y (int): The y coordinate of the SW corner of its surrounding rectangle.
            w (int): The horizontal length of the surrounding rectangle.
            h (int): The vertical length of the surrounding rectangle.
            top (int): The height of the top bar.
            dispatchers (Iterable[Observer]): A collection of dispatchers that the menu
            should listen to. Defaults to an empty tuple.
        """
        Observer.__init__(self, dispatchers)
        self._rect: Rectangle = Rectangle(x, y, w, h)
        self._top: int = top
        self._state: GuiState = state
        self._text_box: TextBox = TextBox(
            RightMenu._INITIAL_MESSAGE,
            RightMenu._FONT_SIZE,
            RightMenu._TEXT_COLOR,
            RightMenu._TEXT_BOX_COLOR,
        )
        self._keyboard: ButtonGrid = ButtonGrid(8, 4)
        self._populate_keyboard()
        self.position(w, h)

    def position(self, x: int, height: int):
        """Position the right bar, after a resize event.

        Args:
            x (int): The x coordinate of the bar's SW position.
            height (int): The height of the bar.
        """
        self._rect.x = x
        self._rect.h = height
        self._text_box.position(
            self._rect.x + RightMenu._PADDING,
            self._rect.h - self._top + RightMenu._PADDING,
            self._rect.w - 2 * RightMenu._PADDING,
            self._top - 2 * RightMenu._PADDING,
        )
        self._keyboard.position(
            self._rect.x, self._rect.y, self._rect.w, self._rect.h - self._top
        )

    ##################
    # Event Handlers #
    ##################

    def on_draw(self) -> None:
        """Draw event handler."""
        GeoDrawer.draw_rectangle(
            self._rect.x,
            self._rect.y,
            self._rect.w,
            self._rect.h,
            RightMenu._BACKGROUND_COLOR,
        )
        self._text_box.draw()
        self._keyboard.draw()

    def on_key_press(self, symbol, _modifiers) -> bool:
        """Key pressed event handler.

        Args:
            symbol (int): The key pressed.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self._text_box.has_focus():
            if symbol == pyglet.window.key.ESCAPE:
                self._text_box.release_focus()
            if symbol == pyglet.window.key.ENTER:
                self._dispatch_input_if_not_empty()
            return True
        return False

    def on_mouse_press(self, x, y, button, _modifiers) -> bool:
        """Mouse click event handler.

        Args:
            x (int): The x coordinate of the click.
            y (int): The y coordinate of the click.
            button (int): The mouse button that was clicked.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if not self._text_box.hit_test(x, y):
            if self._text_box.has_focus():
                self._dispatch_input_if_not_empty()
                return True
        else:
            if self._text_box.has_focus():
                if button == pyglet.window.mouse.RIGHT:
                    self._text_box.add_text(paste())
            else:
                self._text_box.set_focus()
            return False

        self._keyboard.click_check(x, y)
        return False

    def on_text(self, text):
        """Text input event handler. If text box does not have focus, we ignore it.
        All non-printable characters are also ignored.

        Args:
            text (str): The newly written text.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self._text_box.has_focus():
            if text.isprintable():
                self._text_box.add_text(text)
            return True
        return False

    def on_text_motion(self, motion):
        """Text motion event handler.

        Args:
            motion (int): The motion type.

        Returns:
            bool: True if the event is consumed by the handler, false otherwise.
        """
        if self._text_box.has_focus():
            self._text_box.move_text(motion)
            return True
        return False

    ###################
    # Private helpers #
    ###################

    def _dispatch_input_if_not_empty(self):
        """Release focus of text input and dispatch the event of handling it
        if it is non-empty.
        """
        self._text_box.release_focus()
        input_string = self._text_box.get_current_text()
        if input_string:
            self.dispatch_event(CustomEvents.ON_PLACEMENT_INPUT, input_string)

    def _populate_keyboard(self):
        """Populate key grid."""
        self._add_selection_btns()
        self._add_btns()
        self._add_toggle_btns()

    def _add_selection_btns(self):
        """Adds selection buttons to grid."""
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
            self._keyboard.add_btn(*pos, btn)
        self._keyboard.add_selection_group(
            positions,
            on_click=self._state.set_mouse_click_action,
        )

    def _add_btns(self):
        """Adds normal buttons to grid."""
        self._keyboard.add_btn(
            3,
            1,
            Button(
                Images.OBSTR_INF,
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_OBSTRUCTION_INFERRAL
                ),
            ),
        )
        self._keyboard.add_btn(
            3,
            2,
            Button(
                Images.UNDO, on_click=lambda: self.dispatch_event(CustomEvents.ON_UNDO)
            ),
        )
        self._keyboard.add_btn(
            3,
            3,
            Button(
                Images.REDO, on_click=lambda: self.dispatch_event(CustomEvents.ON_REDO)
            ),
        )
        self._keyboard.add_btn(
            2,
            0,
            Button(
                Images.EXPORT,
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_FETCH_TILING_FOR_EXPORT
                ),
            ),
        )
        self._keyboard.add_btn(
            2,
            1,
            Button(
                Images.SEQUENCE,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_PRINT_SEQUENCE),
            ),
        )
        self._keyboard.add_btn(
            2,
            2,
            Button(
                Images.STR,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_PRINT_TILING),
            ),
        )
        self._keyboard.add_btn(
            2,
            3,
            Button(
                Images.VERIFICATION,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_VERIFICATION),
            ),
        )
        self._keyboard.add_btn(
            1,
            2,
            Button(
                Images.TIKZ,
                on_click=lambda: self.dispatch_event(CustomEvents.ON_TIKZ),
            ),
        )
        self._keyboard.add_btn(
            1,
            0,
            Button(
                Images.ROWCOLSEP,
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_ROW_COL_SEPERATION
                ),
            ),
        )
        self._keyboard.add_btn(
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
        """Adds toggle buttons to grid."""
        self._keyboard.add_btn(
            1,
            3,
            ToggleButton(
                Images.HTC,
                on_click=self._state.toggle_highlight_touching_cell,
                toggled=self._state.highlight_touching_cell,
            ),
        )
        self._keyboard.add_btn(
            0,
            0,
            ToggleButton(
                Images.SHADING,
                on_click=self._state.toggle_shading,
                toggled=self._state.shading,
            ),
        )
        self._keyboard.add_btn(
            0,
            1,
            ToggleButton(
                Images.PRETTY,
                on_click=self._state.toggle_pretty_points,
                toggled=self._state.pretty_points,
            ),
        )
        self._keyboard.add_btn(
            0,
            2,
            ToggleButton(
                Images.SHOW_CROSS,
                on_click=self._state.toggle_show_crossing,
                toggled=self._state.show_crossing,
            ),
        )
        self._keyboard.add_btn(
            0,
            3,
            ToggleButton(
                Images.SHOW_LOCAL,
                on_click=self._state.toggle_show_localized,
                toggled=self._state.show_localized,
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
RightMenu.register_event_type(CustomEvents.ON_VERIFICATION)
RightMenu.register_event_type(CustomEvents.ON_TIKZ)
RightMenu.register_event_type(CustomEvents.ON_OBSTRUCTION_INFERRAL)
