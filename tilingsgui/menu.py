import pyglet

from tilings import Tiling

from .events import CustomEvents, Observer
from .geometry import Rectangle
from .graphics import Color, GeoDrawer
from .state import GuiState
from .utils import paste
from .widgets import Button, ButtonGrid, SelectionButton, TextBox, ToggleButton


class TopMenu(pyglet.event.EventDispatcher, Observer):
    PADDING = 1
    INITIAL_MESSAGE = " -- Basis here -- e.g. 1234_1324"
    FONT_SIZE = 12
    TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    TEXT_BOX_COLOR = Color.DARK_GRAY
    BACKGROUND_COLOR = Color.BLACK

    def __init__(self, x, y, w, h, dispatchers):
        Observer.__init__(self, dispatchers)
        self.rect = Rectangle(x, y, w, h)
        self.text_box = TextBox(
            TopMenu.INITIAL_MESSAGE,
            TopMenu.FONT_SIZE,
            TopMenu.TEXT_COLOR,
            TopMenu.TEXT_BOX_COLOR,
        )
        self.position(w, h)

    def on_draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.rect.x, self.rect.y, self.rect.w, self.rect.h, TopMenu.BACKGROUND_COLOR
        )
        self.text_box.draw()

    def position(self, width, height):
        self.rect.w = width
        self.rect.y = height
        self.text_box.position(
            self.rect.x + TopMenu.PADDING,
            self.rect.y + TopMenu.PADDING,
            self.rect.w - 2 * TopMenu.PADDING,
            self.rect.h - 2 * TopMenu.PADDING,
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
    INITIAL_MESSAGE = "12"
    FONT_SIZE = 12
    TEXT_COLOR = Color.alpha_extend(Color.BLACK)
    TEXT_BOX_COLOR = Color.DARK_GRAY
    BACKGROUND_COLOR = Color.BLACK

    def __init__(self, x, y, w, h, t, state: GuiState, dispatchers):
        Observer.__init__(self, dispatchers)
        self.rect = Rectangle(x, y, w, h)
        self.t = t

        self.state = state

        self.text_box = TextBox(
            RightMenu.INITIAL_MESSAGE,
            RightMenu.FONT_SIZE,
            RightMenu.TEXT_COLOR,
            RightMenu.TEXT_BOX_COLOR,
        )

        self.keyboard = ButtonGrid(10, 4)

        # Select grp
        # TODO: Collect these into variables
        self.keyboard.add_btn(9, 0, SelectionButton("add_point.png", toggled=True))
        self.keyboard.add_btn(9, 1, SelectionButton("add_custom.png"))
        self.keyboard.add_btn(9, 2, SelectionButton("factor.png"))
        self.keyboard.add_btn(9, 3, SelectionButton("factor_int.png"))
        self.keyboard.add_btn(8, 0, SelectionButton("place_west.png"))
        self.keyboard.add_btn(8, 1, SelectionButton("place_east.png"))
        self.keyboard.add_btn(8, 2, SelectionButton("place_north.png"))
        self.keyboard.add_btn(8, 3, SelectionButton("place_south.png"))
        self.keyboard.add_btn(7, 0, SelectionButton("pplace_west.png"))
        self.keyboard.add_btn(7, 1, SelectionButton("pplace_east.png"))
        self.keyboard.add_btn(7, 2, SelectionButton("pplace_north.png"))
        self.keyboard.add_btn(7, 3, SelectionButton("pplace_south.png"))
        self.keyboard.add_btn(6, 0, SelectionButton("fusion_r.png"))
        self.keyboard.add_btn(6, 1, SelectionButton("fusion_c.png"))
        self.keyboard.add_btn(6, 2, SelectionButton("fusion_comp_r.png"))
        self.keyboard.add_btn(6, 3, SelectionButton("fusion_comp_c.png"))
        self.keyboard.add_btn(5, 0, SelectionButton("move.png"))

        self.keyboard.add_selection_group(
            [
                (9, 0),
                (9, 1),
                (9, 2),
                (9, 3),
                (8, 0),
                (8, 1),
                (8, 2),
                (8, 3),
                (7, 0),
                (7, 1),
                (7, 2),
                (7, 3),
                (6, 0),
                (6, 1),
                (6, 2),
                (6, 3),
                (5, 0),
            ],
            on_click=self.state.set_strategy,
        )

        # normal btns
        self.keyboard.add_btn(
            4,
            0,
            Button(
                "undo.png", on_click=lambda: self.dispatch_event(CustomEvents.ON_UNDO)
            ),
        )
        self.keyboard.add_btn(
            4,
            1,
            Button(
                "redo.png", on_click=lambda: self.dispatch_event(CustomEvents.ON_REDO)
            ),
        )
        self.keyboard.add_btn(
            4,
            2,
            Button(
                "str.png",
                on_click=lambda: self.dispatch_event(CustomEvents.ON_PRINT_TILING),
            ),
        ),
        self.keyboard.add_btn(
            4,
            3,
            Button(
                "verification.png",
                on_click=lambda: self.dispatch_event(CustomEvents.ON_VERTIFICATION),
            ),
        )
        self.keyboard.add_btn(
            3,
            0,
            Button(
                "rowcolsep.png",
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_ROW_COL_SEPERATION
                ),
            ),
        )
        self.keyboard.add_btn(
            3,
            1,
            Button(
                "obstr-trans.png",
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_OBSTRUCTION_TRANSIVITY
                ),
            ),
        )
        self.keyboard.add_btn(
            3,
            2,
            Button(
                "export.png",
                on_click=lambda: self.dispatch_event(
                    CustomEvents.ON_FETCH_TILING_FOR_EXPORT
                ),
            ),
        )
        self.keyboard.add_btn(
            3,
            3,
            Button(
                "sequence.png",
                on_click=lambda: self.dispatch_event(CustomEvents.ON_PRINT_SEQUENCE),
            ),
        )

        # toggle btns
        self.keyboard.add_btn(
            1,
            0,
            ToggleButton(
                "shading.png",
                on_click=self.state.toggle_shading,
                toggled=self.state.shading,
            ),
        )
        self.keyboard.add_btn(
            1,
            1,
            ToggleButton(
                "pretty.png",
                on_click=self.state.toggle_pretty_points,
                toggled=self.state.pretty_points,
            ),
        )
        self.keyboard.add_btn(
            1,
            2,
            ToggleButton(
                "show_cross.png",
                on_click=self.state.toggle_show_crossing,
                toggled=self.state.show_crossing,
            ),
        )
        self.keyboard.add_btn(
            1,
            3,
            ToggleButton(
                "show_local.png",
                on_click=self.state.toggle_show_localized,
                toggled=self.state.show_localized,
            ),
        )
        self.keyboard.add_btn(
            0,
            0,
            ToggleButton(
                "htc.png",
                on_click=self.state.toggle_highlight_touching_cell,
                toggled=self.state.highlight_touching_cell,
            ),
        )

        self.position(w, h)

    def on_draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.rect.x,
            self.rect.y,
            self.rect.w,
            self.rect.h,
            RightMenu.BACKGROUND_COLOR,
        )
        self.text_box.draw()
        self.keyboard.draw()

    def position(self, width, height):
        self.rect.x = width
        self.rect.h = height
        self.text_box.position(
            self.rect.x + TopMenu.PADDING,
            self.rect.h - self.t + TopMenu.PADDING,
            self.rect.w - 2 * TopMenu.PADDING,
            self.t - 2 * TopMenu.PADDING,
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
            self.text_box.on_text(text)
            return True
        return False

    def on_text_motion(self, motion):
        if self.text_box.has_focus():
            self.text_box.on_text_motion(motion)
            return True
        return False


RightMenu.register_event_type(CustomEvents.ON_PLACEMENT_INPUT)
RightMenu.register_event_type(CustomEvents.ON_FETCH_TILING_FOR_EXPORT)
RightMenu.register_event_type(CustomEvents.ON_UNDO)
RightMenu.register_event_type(CustomEvents.ON_REDO)
RightMenu.register_event_type(CustomEvents.ON_ROW_COL_SEPERATION)
RightMenu.register_event_type(CustomEvents.ON_OBSTRUCTION_TRANSIVITY)
RightMenu.register_event_type(CustomEvents.ON_PRINT_SEQUENCE)
RightMenu.register_event_type(CustomEvents.ON_PRINT_TILING)
RightMenu.register_event_type(CustomEvents.ON_VERTIFICATION)
