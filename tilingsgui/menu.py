import pyglet
import pyperclip
from tilingsgui.graphics import Color, GeoDrawer
from tilingsgui.state import GuiState
from tilingsgui.utils import paste
from tilingsgui.widgets import (
    Button,
    SelectButton,
    SelectButtonGroup,
    TextBox,
    ToggleButton,
)


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

        self.sel_grp = SelectButtonGroup()
        self.sel_grp.add_button(SelectButton("●"))
        self.sel_grp.add_button(SelectButton("⛬"))
        self.sel_grp.add_button(SelectButton("F"))
        self.sel_grp.add_button(SelectButton("⏪"))
        self.sel_grp.add_button(SelectButton("⏩"))
        self.sel_grp.add_button(SelectButton("⏫"))
        self.sel_grp.add_button(SelectButton("⏬"))
        self.sel_grp.add_button(SelectButton("⬅"))
        self.sel_grp.add_button(SelectButton("➡"))
        self.sel_grp.add_button(SelectButton("⬆"))
        self.sel_grp.add_button(SelectButton("⬇"))

        self.on_resize(w, h)

    def draw(self):
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, Color.BLACK)
        self.text_box.draw()
        self.sel_grp.draw()

    def on_resize(self, width, height):
        self.x = width
        self.h = height
        self.text_box.position(
            self.x + TopMenu.PADDING,
            self.h - self.t + TopMenu.PADDING,
            self.w - 2 * TopMenu.PADDING,
            self.t - 2 * TopMenu.PADDING,
        )
        self.position_buttons()

    def position_buttons(self):
        self.sel_grp.buttons[0].position(self.x + 1, self.h - self.t - 50 + 1, 48, 48)
        self.sel_grp.buttons[1].position(
            self.x + 1 + 50, self.h - self.t - 50 + 1, 48, 48
        )
        self.sel_grp.buttons[2].position(
            self.x + 1 + 100, self.h - self.t - 50 + 1, 48, 48
        )
        self.sel_grp.buttons[3].position(
            self.x + 1, self.h - self.t - 50 + 1 - 50 * 1, 48, 48
        )
        self.sel_grp.buttons[4].position(
            self.x + 1 + 50, self.h - self.t - 50 + 1 - 50 * 1, 48, 48
        )
        self.sel_grp.buttons[5].position(
            self.x + 1 + 100, self.h - self.t - 50 + 1 - 50 * 1, 48, 48
        )
        self.sel_grp.buttons[6].position(
            self.x + 1 + 150, self.h - self.t - 50 + 1 - 50 * 1, 48, 48
        )
        self.sel_grp.buttons[7].position(
            self.x + 1, self.h - self.t - 50 + 1 - 50 * 2, 48, 48
        )
        self.sel_grp.buttons[8].position(
            self.x + 1 + 50, self.h - self.t - 50 + 1 - 50 * 2, 48, 48
        )
        self.sel_grp.buttons[9].position(
            self.x + 1 + 100, self.h - self.t - 50 + 1 - 50 * 2, 48, 48
        )
        self.sel_grp.buttons[10].position(
            self.x + 1 + 150, self.h - self.t - 50 + 1 - 50 * 2, 48, 48
        )

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

    def on_text(self, text):
        if self.state.cell_input_focus:
            self.text_box.on_text(text)

    def on_text_motion(self, motion):
        if self.state.cell_input_focus:
            self.text_box.on_text_motion(motion)
