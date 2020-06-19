import pyglet

from .graphics import Color, GeoDrawer
from .state import GuiState
from .utils import paste
from .widgets import Button, ButtonGrid, SelectionButton, TextBox, ToggleButton


class TopMenu:
    PADDING = 1
    INITIAL_MESSAGE = " -- Basis here -- e.g. 1234_1324"

    def __init__(self, x, y, w, h, state: GuiState):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = state
        self.text_box = TextBox(TopMenu.INITIAL_MESSAGE)
        self.on_resize(w, h)

    def draw(self):
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, Color.BLACK)
        self.text_box.draw()

    def on_resize(self, width, height):
        self.w = width
        self.y = height
        self.text_box.position(
            self.x + TopMenu.PADDING,
            self.y + TopMenu.PADDING,
            self.w - 2 * TopMenu.PADDING,
            self.h - 2 * TopMenu.PADDING,
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.text_box.release_focus()
            self.state.basis_input_focus = False
        if symbol == pyglet.window.key.ENTER:
            self.text_box.release_focus()
            self.state.basis_input_focus = False
            s = self.text_box.get_current_text()
            if s:
                self.state.basis_input_read = True
                self.state.basis_input_string = s

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.text_box.hit_test(x, y):
            if self.state.basis_input_focus:
                s = self.text_box.get_current_text()
                if s:
                    self.state.basis_input_read = True
                    self.state.basis_input_string = s
                self.text_box.release_focus()
                self.state.basis_input_focus = False
            return
        if self.state.basis_input_focus:
            if button == pyglet.window.mouse.RIGHT:
                self.text_box.append_text(paste())
        else:
            self.state.basis_input_focus = True
            self.text_box.set_focus()

    def on_text(self, text):
        if self.state.basis_input_focus:
            self.text_box.on_text(text)

    def on_text_motion(self, motion):
        if self.state.basis_input_focus:
            self.text_box.on_text_motion(motion)


class RightMenu:
    def __init__(self, x, y, w, h, t, state: GuiState):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t

        self.state = state

        self.text_box = TextBox("single cell requirement")

        self.keyboard = ButtonGrid(x, y, w, h - t, 10, 4)

        # Select grp

        self.keyboard.add_btn(9, 0, SelectionButton("add_point.png", toggled=True))
        self.keyboard.add_btn(9, 1, SelectionButton("add_custom.png"))
        self.keyboard.add_btn(9, 2, SelectionButton("factor.png"))
        self.keyboard.add_btn(9, 3, SelectionButton("move.png"))
        self.keyboard.add_btn(8, 0, SelectionButton("place_west.png"))
        self.keyboard.add_btn(8, 1, SelectionButton("place_east.png"))
        self.keyboard.add_btn(8, 2, SelectionButton("place_north.png"))
        self.keyboard.add_btn(8, 3, SelectionButton("place_south.png"))
        self.keyboard.add_btn(7, 0, SelectionButton("pplace_west.png"))
        self.keyboard.add_btn(7, 1, SelectionButton("pplace_east.png"))
        self.keyboard.add_btn(7, 2, SelectionButton("pplace_north.png"))
        self.keyboard.add_btn(7, 3, SelectionButton("pplace_south.png"))
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
            ],
            on_click=self.state.set_strategy,
        )

        # normal btns
        self.keyboard.add_btn(5, 0, Button("undo.png", on_click=self.state.set_undo))
        self.keyboard.add_btn(5, 1, Button("redo.png", on_click=self.state.set_redo))
        self.keyboard.add_btn(
            4, 0, Button("rowcolsep.png", on_click=self.state.set_row_col_seperation)
        )
        self.keyboard.add_btn(
            4,
            1,
            Button("obstr-trans.png", on_click=self.state.set_obstruction_transivity),
        )
        self.keyboard.add_btn(
            4, 2, Button("export.png", on_click=self.state.set_export)
        )

        # toggle btns
        self.keyboard.add_btn(
            2,
            0,
            ToggleButton(
                "shading.png",
                on_click=self.state.toggle_shading,
                toggled=self.state.shading,
            ),
        )
        self.keyboard.add_btn(
            2,
            1,
            ToggleButton(
                "pretty.png",
                on_click=self.state.toggle_pretty_points,
                toggled=self.state.pretty_points,
            ),
        )
        self.keyboard.add_btn(
            2,
            2,
            ToggleButton(
                "show_cross.png",
                on_click=self.state.toggle_show_crossing,
                toggled=self.state.show_crossing,
            ),
        )
        self.keyboard.add_btn(
            2,
            3,
            ToggleButton(
                "show_local.png",
                on_click=self.state.toggle_show_localized,
                toggled=self.state.show_localized,
            ),
        )
        self.keyboard.add_btn(
            1,
            0,
            ToggleButton(
                "htc.png",
                on_click=self.state.toggle_highlight_touching_cell,
                toggled=self.state.highlight_touching_cell,
            ),
        )

        self.on_resize(w, h)

    def draw(self):
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, Color.BLACK)
        self.text_box.draw()
        self.keyboard.draw()

    def on_resize(self, width, height):
        self.x = width
        self.h = height
        self.text_box.position(
            self.x + TopMenu.PADDING,
            self.h - self.t + TopMenu.PADDING,
            self.w - 2 * TopMenu.PADDING,
            self.t - 2 * TopMenu.PADDING,
        )
        self.keyboard.resize(self.x, self.y, self.w, self.h - self.t)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.text_box.release_focus()
            self.state.cell_input_focus = False
        if symbol == pyglet.window.key.ENTER:
            self.text_box.release_focus()
            self.state.cell_input_focus = False
            s = self.text_box.get_current_text()
            if s:
                self.state.cell_input_read = True
                self.state.cell_input_string = s

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.text_box.hit_test(x, y):
            if self.state.cell_input_focus:
                s = self.text_box.get_current_text()
                if s:
                    self.state.cell_input_read = True
                    self.state.cell_input_string = s
                self.text_box.release_focus()
                self.state.cell_input_focus = False
                return
        else:
            if self.state.cell_input_focus:
                if button == pyglet.window.mouse.RIGHT:
                    self.text_box.append_text(paste())
            else:
                self.state.cell_input_focus = True
                self.text_box.set_focus()
            return

        self.keyboard.click_check(x, y)

    def on_text(self, text):
        if self.state.cell_input_focus:
            self.text_box.on_text(text)

    def on_text_motion(self, motion):
        if self.state.cell_input_focus:
            self.text_box.on_text_motion(motion)
