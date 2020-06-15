import pyglet
import pyperclip

from tilingsgui.graphics import Color, GeoDrawer
from tilingsgui.widgets import TextBox


class TopMenu:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text_box = TextBox("Write basis here...", x + 1, y + 1, w - 2, h - 2)
        self.string_to_process = []

    def draw(self):
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, Color.BLACK)
        self.text_box.draw()

    def on_resize(self, width, height):
        self.w = width
        self.y = height
        self.text_box.resize(width - 2, height + 1)

    def has_focus(self):
        return self.text_box.focused

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.text_box.release_focus()
        if symbol == pyglet.window.key.ENTER:
            self.text_box.release_focus()
            s = self.text_box.get_current_text()
            if s:
                self.string_to_process.append(s)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.text_box.hit_test(x, y):
            if self.text_box.focused:
                s = self.text_box.get_current_text()
                if s:
                    self.string_to_process.append(s)
                self.text_box.release_focus()

            return
        if self.has_focus():
            if button == pyglet.window.mouse.RIGHT:
                paste = pyperclip.paste()
                if paste:
                    self.text_box.append_text(paste)
        else:
            self.text_box.set_focus()

    def on_text(self, text):
        if self.text_box.focused:
            self.text_box.on_text(text)

    def on_text_motion(self, motion):
        if self.text_box.focused:
            self.text_box.on_text_motion(motion)

    def get_input_text(self):
        if self.text_box.focused:
            return self.text_box.get_current_text()


class RightMenu:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.x, self.y, self.w, self.h, Color.GREEN_YELLOW
        )

    def on_resize(self, width, height):
        self.x = width
        self.h = height

    def has_focus(self):
        return False
