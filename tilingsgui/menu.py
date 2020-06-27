"""Control stations.
"""

import pyglet

from tilings import Tiling

from .events import CustomEvents, Observer
from .files import Images
from .geometry import Rectangle
from .graphics import Color, GeoDrawer
from .state import GuiState
from .utils import paste
from .widgets import Button, ButtonGrid, SelectionButton, TextBox, ToggleButton

# RGB = Tuple[float, float, float]
# RGBA = Tuple[float, float, float, float]


class TopMenu(pyglet.event.EventDispatcher, Observer):
    _PADDING = 1
    _INITIAL_MESSAGE = " -- Basis here -- e.g. 1234_1324"
    _FONT_SIZE = 12
    _TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    _TEXT_BOX_COLOR = Color.DARK_GRAY
    _BACKGROUND_COLOR = Color.BLACK

    def __init__(self, x, y, w, h, dispatchers):
        Observer.__init__(self, dispatchers)
        self.rect = Rectangle(x, y, w, h)
        self.text_box = TextBox(
            TopMenu._INITIAL_MESSAGE,
            TopMenu._FONT_SIZE,
            TopMenu._TEXT_COLOR,
            TopMenu._TEXT_BOX_COLOR,
        )
        self.position(w, h)

    def on_draw(self):
        GeoDrawer.draw_rectangle(
            self.rect.x,
            self.rect.y,
            self.rect.w,
            self.rect.h,
            TopMenu._BACKGROUND_COLOR,
        )
        self.text_box.draw()

    def position(self, width, height):
        self.rect.w = width
        self.rect.y = height
        self.text_box.position(
            self.rect.x + TopMenu._PADDING,
            self.rect.y + TopMenu._PADDING,
            self.rect.w - 2 * TopMenu._PADDING,
            self.rect.h - 2 * TopMenu._PADDING,
        )

    def on_key_press(self, symbol, modifiers):
        if self.text_box.has_focus():
            if symbol == pyglet.window.key.ESCAPE:
                self.text_box.release_focus()
            elif symbol == pyglet.window.key.ENTER:
                self.text_box.release_focus()
                input_string = self.text_box.get_current_text()
                if input_string:
                    if input_string[0] == "{" and input_string[-1] == "}":
                        try:
                            tiling = Tiling.from_json(input_string)
                            self.dispatch_event(
                                CustomEvents.ON_BASIS_JSON_INPUT, tiling
                            )
                            return True
                        except ValueError:
                            pass
                    self.dispatch_event(CustomEvents.ON_BASIS_INPUT, input_string)
            return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.text_box.hit_test(x, y):
            if self.text_box.has_focus():
                self.text_box.release_focus()
                input_string = self.text_box.get_current_text()
                if input_string:
                    if input_string[0] == "{" and input_string[-1] == "}":
                        try:
                            tiling = Tiling.from_json(input_string)
                            self.dispatch_event(
                                CustomEvents.ON_BASIS_JSON_INPUT, tiling
                            )
                            return True
                        except (ValueError, KeyError):
                            pass
                    self.dispatch_event(CustomEvents.ON_BASIS_INPUT, input_string)
                return True
            return False
        if self.text_box.has_focus():
            if button == pyglet.window.mouse.RIGHT:
                self.text_box.append_text(paste())
        else:
            self.text_box.set_focus()
        return False

    def on_text(self, text):
        if self.text_box.has_focus():
            if text.isprintable():
                self.text_box.on_text(text)
            return True
        return False

    def on_text_motion(self, motion):
        if self.text_box.has_focus():
            self.text_box.on_text_motion(motion)
            return True
        return False


TopMenu.register_event_type(CustomEvents.ON_BASIS_INPUT)
TopMenu.register_event_type(CustomEvents.ON_BASIS_JSON_INPUT)


#####################################
#####################################
#####################################
#####################################
#####################################
######################################


class RightMenu(pyglet.event.EventDispatcher, Observer):
    _PADDING = 1
    _INITIAL_MESSAGE = "12"
    _FONT_SIZE = 12
    _TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    _TEXT_BOX_COLOR = Color.DARK_GRAY
    _BACKGROUND_COLOR = Color.BLACK

    def __init__(self, x, y, w, h, t, state: GuiState, dispatchers):
        Observer.__init__(self, dispatchers)
        self.rect = Rectangle(x, y, w, h)
        self.t = t
        self.state = state
        self.text_box = TextBox(
            RightMenu._INITIAL_MESSAGE,
            RightMenu._FONT_SIZE,
            RightMenu._TEXT_COLOR,
            RightMenu._TEXT_BOX_COLOR,
        )
        self.keyboard = ButtonGrid(8, 4)
        self._populate_keyboard()
        self.position(w, h)

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

    def position(self, width, height):
        self.rect.x = width
        self.rect.h = height
        self.text_box.position(
            self.rect.x + RightMenu._PADDING,
            self.rect.h - self.t + RightMenu._PADDING,
            self.rect.w - 2 * RightMenu._PADDING,
            self.t - 2 * RightMenu._PADDING,
        )
        self.keyboard.resize(
            self.rect.x, self.rect.y, self.rect.w, self.rect.h - self.t
        )

    def on_key_press(self, symbol, modifiers):

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

    def on_mouse_press(self, x, y, button, modifiers):
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
                    self.text_box.append_text(paste())
            else:
                self.text_box.set_focus()
            return False

        self.keyboard.click_check(x, y)

    def on_text(self, text):
        if self.text_box.has_focus():
            if text.isprintable():
                self.text_box.on_text(text)
            return True
        return False

    def on_text_motion(self, motion):
        if self.text_box.has_focus():
            self.text_box.on_text_motion(motion)
            return True
        return False

    def _populate_keyboard(self):
        self._add_selection_btns()
        self._add_btns()
        self._add_toggle_btns()

    def _add_selection_btns(self):
        self.keyboard.add_btn(7, 0, SelectionButton(Images.ADD_POINT, toggled=True))
        self.keyboard.add_btn(7, 1, SelectionButton(Images.ADD_CUSOM))
        self.keyboard.add_btn(7, 2, SelectionButton(Images.FACTOR))
        self.keyboard.add_btn(7, 3, SelectionButton(Images.FACTOR_INT))
        self.keyboard.add_btn(6, 0, SelectionButton(Images.PLACE_WEST))
        self.keyboard.add_btn(6, 1, SelectionButton(Images.PLACE_EAST))
        self.keyboard.add_btn(6, 2, SelectionButton(Images.PLACE_NORTH))
        self.keyboard.add_btn(6, 3, SelectionButton(Images.PLACE_SOUTH))
        self.keyboard.add_btn(5, 0, SelectionButton(Images.PPLACE_WEST))
        self.keyboard.add_btn(5, 1, SelectionButton(Images.PPLACE_EAST))
        self.keyboard.add_btn(5, 2, SelectionButton(Images.PPLACE_NORTH))
        self.keyboard.add_btn(5, 3, SelectionButton(Images.PPLACE_SOUTH))
        self.keyboard.add_btn(4, 0, SelectionButton(Images.FUSION_R))
        self.keyboard.add_btn(4, 1, SelectionButton(Images.FUSION_C))
        self.keyboard.add_btn(4, 2, SelectionButton(Images.FUSION_COM_R))
        self.keyboard.add_btn(4, 3, SelectionButton(Images.FUSION_COM_C))
        self.keyboard.add_btn(3, 0, SelectionButton(Images.MOVE))

        self.keyboard.add_selection_group(
            [
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
            ],
            on_click=self.state.set_mouse_click_action,
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
