import pyglet
import pyperclip
from tilingsgui.graphics import Color, GeoDrawer
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

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text_box = TextBox(TopMenu.INITIAL_MESSAGE)
        self.string_to_process = ""
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

    def has_focus(self):
        return self.text_box.has_focus()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.text_box.release_focus()
        if symbol == pyglet.window.key.ENTER:
            self.text_box.release_focus()
            s = self.text_box.get_current_text()
            if s:
                self.string_to_process = s
                return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.text_box.hit_test(x, y):
            if self.text_box.has_focus():
                s = self.text_box.get_current_text()
                if s:
                    self.string_to_process = s
                    return True
                self.text_box.release_focus()
            return False
        if self.text_box.has_focus():
            if button == pyglet.window.mouse.RIGHT:
                try:
                    paste = pyperclip.paste()
                    if paste:
                        self.text_box.append_text(paste)
                except pyperclip.PyperclipException:
                    # Console log something?
                    # Most likely on linux:
                    # sudo apt-get install xclip
                    # sudo apt-get install xsel
                    pass
        else:
            self.text_box.set_focus()
        return False

    def on_text(self, text):
        if self.text_box.has_focus():
            self.text_box.on_text(text)

    def on_text_motion(self, motion):
        if self.text_box.has_focus():
            self.text_box.on_text_motion(motion)

    def read_from_textbox(self):
        return self.string_to_process


class RightMenu:
    def __init__(self, x, y, w, h, t):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t
        self.text_box_height = t

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

        """
        self.rcs = Button("RCS", x + 1, h - t - 50 + 1 - 50 * 6 - 10, 48, 48)
        self.ot = Button("OT", x + 1 + 50, h - t - 50 + 1 - 50 * 6 - 10, 48, 48)
        self.undo = Button("⟲", x + 1, h - t - 50 + 1 - 50 * 7 - 10, 48, 48)
        self.redo = Button("⟳", x + 1 + 50, h - t - 50 + 1 - 50 * 7 - 10, 48, 48)

        self.shading = ToggleButton("S", x + 1, h - t - 50 + 1 - 50 * 8 - 20, 48, 48)
        self.pretty_points = ToggleButton(
            "PP", x + 1 + 50, h - t - 50 + 1 - 50 * 8 - 20, 48, 48
        )
        self.show_crossing = ToggleButton(
            "SC", x + 1, h - t - 50 + 1 - 50 * 9 - 20, 48, 48
        )
        self.show_localized = ToggleButton(
            "SL", x + 1 + 50, h - t - 50 + 1 - 50 * 9 - 20, 48, 48
        )
        self.highlight_touching_cell = ToggleButton(
            "HTC", x + 1, h - t - 50 + 1 - 50 * 10 - 20, 48, 48
        )"""

    def draw(self):
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, Color.BLACK)
        self.text_box.draw()
        self.sel_grp.draw()
        """self.rcs.draw()
        self.ot.draw()
        self.undo.draw()
        self.redo.draw()
        self.shading.draw()
        self.pretty_points.draw()
        self.show_crossing.draw()
        self.show_localized.draw()
        self.highlight_touching_cell.draw()"""

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

    def has_focus(self):
        return False
