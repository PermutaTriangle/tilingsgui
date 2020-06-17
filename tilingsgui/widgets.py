from typing import List

import pyglet
from tilingsgui.graphics import Color, GeoDrawer


class TextBox:
    def __init__(self, init_text, x=0, y=0, width=0, height=0):
        self.document = pyglet.text.document.UnformattedDocument(init_text)
        self.document.set_style(
            0, len(self.document.text), dict(font_size=12, color=(0, 0, 0, 255))
        )
        self.batch = pyglet.graphics.Batch()
        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=self.batch
        )
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.vertex_list = self.batch.add(
            4,
            pyglet.gl.GL_QUADS,
            None,
            ("v2f", [x, y, x + width, y, x + width, y + height, x, y + height]),
            ("c3B", Color.DARK_GRAY * 4),
        )
        self.caret.visible = False
        self.position(x, y, width, height)

    def position(self, x, y, w, h):
        for i, vertex in enumerate((x, y, x + w, y, x + w, y + h, x, y + h)):
            self.vertex_list.vertices[i] = vertex
        self.layout.x = x + 5
        self.layout.y = y
        self.layout.width = w
        self.layout.height = h

    def draw(self):
        self.batch.draw()

    def hit_test(self, x, y):
        return (
            0 < x - self.layout.x < self.layout.width
            and 0 < y - self.layout.y < self.layout.height
        )

    def on_text(self, text):
        self.caret.on_text(text)

    def on_text_motion(self, motion):
        self.caret.on_text_motion(motion)

    def has_focus(self):
        return self.caret.visible

    def set_focus(self):
        self.document.text = ""
        self.caret.visible = True

    def release_focus(self):
        self.caret.visible = False
        self.caret.mark = self.caret.position = 0

    def get_current_text(self):
        return self.document.text

    def append_text(self, text):
        self.document.text = self.document.text + text
        self.caret.mark = self.caret.position = len(self.document.text)


# TODO: Make sprite and font subclasses...
class Button:
    FONT_SIZE = 15
    FONT = "Times New Roman"
    LABEL_COLOR = Color.alpha_extend(Color.BLACK)
    BUTTON_COLOR = Color.GRAY

    def __init__(self, text, x=0, y=0, w=0, h=0, on_click=None):
        self.label = pyglet.text.Label(
            text,
            font_size=Button.FONT_SIZE,
            font_name=Button.FONT,
            anchor_x="center",
            anchor_y="center",
            color=Button.LABEL_COLOR,
        )
        self.x, self.y, self.w, self.h = x, y, w, h
        self.position(x, y, w, h)
        self.on_click = on_click

    def hit(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def click_check(self, x, y):
        if self.hit(x, y):
            if self.on_click is not None:
                self.on_click()
            return True
        return False

    def draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.x, self.y, self.w, self.h, Button.BUTTON_COLOR
        )
        self.label.draw()

    def position(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label.x = x + w / 2
        self.label.y = y + h / 2


class ToggleButton(Button):
    def __init__(self, text, x=0, y=0, w=0, h=0, on_click=None, toggled=False):
        super().__init__(text, x, y, w, h, on_click)
        self.toggled = toggled

    def click_check(self, x, y):
        if self.hit(x, y):
            if self.on_click is not None:
                self.toggled = not self.toggled
                self.on_click()
            return True
        return False

    def draw(self):
        color = Color.DARK_OLIVE_GREEN if self.toggled else Button.BUTTON_COLOR
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, color)
        self.label.draw()


class SelectionButton(ToggleButton):
    def __init__(self, text, x=0, y=0, w=0, h=0, toggled=False):
        super().__init__(text, x, y, w, h, on_click=None, toggled=toggled)

    def click_check(self, x, y):
        if self.hit(x, y):
            self.toggled = True
            return True
        return False


class SelectionGroup:
    def __init__(self, grp, on_click, selected=0):
        self.rc_to_i = {(r, c): i for i, (r, c) in enumerate(grp)}
        self.i_to_rc = grp
        self.on_click = on_click
        self.selected = selected

    def __contains__(self, key):
        return key in self.rc_to_i


class ButtonGrid:
    PADDING = 1

    def __init__(self, x, y, w, h, r, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.buttons: List[List[Button]] = [[None for _ in range(c)] for _ in range(r)]
        self.button_w = w / c
        self.button_h = h / r
        self.selection_groups = []

    def add_selection_group(self, grp, on_click):
        self.selection_groups.append(SelectionGroup(grp, on_click))

    def selection_group_event(self, s_grp, r, c):
        _r, _c = s_grp.i_to_rc[s_grp.selected]
        if _r == r and _c == c:
            return
        print(r, c, _r, _c)
        self.buttons[_r][_c].toggled = not self.buttons[_r][_c].toggled
        s_grp.selected = s_grp.rc_to_i[(r, c)]
        s_grp.on_click(s_grp.selected)

    def resize(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.button_w = w / len(self.buttons[0])
        self.button_h = h / len(self.buttons)
        self.position_btns()

    def add_btn(self, r, c, btn):
        self.buttons[r][c] = btn

    def draw(self):
        for row in self.buttons:
            for button in row:
                if button is not None:
                    button.draw()

    def position_btns(self):
        for _r, row in enumerate(self.buttons):
            for _c, btn in enumerate(row):
                if btn is not None:
                    self.place_btn_within_grid(btn, _r, _c)

    def place_btn_within_grid(self, btn, r, c):
        btn.position(
            self.x + self.button_w * c + ButtonGrid.PADDING,
            self.y + self.button_h * r + ButtonGrid.PADDING,
            self.button_w - 2 * ButtonGrid.PADDING,
            self.button_h - 2 * ButtonGrid.PADDING,
        )

    def click_check(self, x, y):
        for _r, row in enumerate(self.buttons):
            for _c, btn in enumerate(row):
                if btn is None:
                    continue
                if btn.click_check(x, y):
                    for s_grp in self.selection_groups:
                        if (_r, _c) in s_grp:
                            self.selection_group_event(s_grp, _r, _c)
                            break
                    return
