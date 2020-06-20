from typing import ClassVar, List

import pyglet

from .graphics import Color, GeoDrawer


class Text:
    LEFT_PAD: ClassVar[int] = 5

    def __init__(self, init_text, font_size, color, batch):
        self.document = pyglet.text.document.UnformattedDocument(init_text)
        self.document.set_style(0, 0, dict(font_size=font_size, color=color))
        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, 0, 0, multiline=False, batch=batch
        )
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.caret.visible = False

    def position(self, x, y, w, h):
        self.layout.x = x + Text.LEFT_PAD
        self.layout.y = y
        self.layout.width = w - Text.LEFT_PAD
        self.layout.height = h


class TextBox:
    def __init__(self, init_text, font_size, text_color, box_color):
        self.batch = pyglet.graphics.Batch()
        self.txt = Text(init_text, font_size, text_color, self.batch)
        self.vertex_list = self.batch.add(
            4, pyglet.gl.GL_QUADS, None, ("v2f", [0] * 8), ("c3B", box_color * 4),
        )

    def position(self, x, y, w, h):
        for i, vertex in enumerate((x, y, x + w, y, x + w, y + h, x, y + h)):
            self.vertex_list.vertices[i] = vertex
        self.txt.position(x, y, w, h)

    def draw(self):
        self.batch.draw()

    def hit_test(self, x, y):
        return (
            self.vertex_list.vertices[0] < x < self.vertex_list.vertices[2]
            and self.vertex_list.vertices[1] < y < self.vertex_list.vertices[5]
        )

    def on_text(self, text):
        self.txt.caret.on_text(text)

    def on_text_motion(self, motion):
        self.txt.caret.on_text_motion(motion)

    def has_focus(self):
        return self.txt.caret.visible

    def set_focus(self):
        self.txt.document.text = ""
        self.txt.caret.visible = True

    def release_focus(self):
        self.txt.caret.visible = False
        self.txt.caret.mark = self.txt.caret.position = 0

    def get_current_text(self):
        return self.txt.document.text

    def append_text(self, text):
        self.txt.document.text = self.txt.document.text + text
        self.txt.caret.mark = self.txt.caret.position = len(self.txt.document.text)


class Button:
    BUTTON_COLOR = Color.GRAY

    def __init__(self, image, on_click=None):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image(image), x=0, y=0)
        self.x, self.y, self.w, self.h = (0,) * 4
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
        self.sprite.draw()

    def position(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        dim = min(w, h)
        if dim > 0:
            self.sprite.scale *= dim / self.sprite.width
            self.sprite.x = x + self.w / 2 - self.sprite.width / 2
            self.sprite.y = y + self.h / 2 - self.sprite.height / 2


class ToggleButton(Button):
    TOGGLE_COLOR = Color.DARK_OLIVE_GREEN

    def __init__(self, text, on_click=None, toggled=False):
        super().__init__(text, on_click)
        self.toggled = toggled

    def click_check(self, x, y):
        if self.hit(x, y):
            if self.on_click is not None:
                self.toggled = not self.toggled
                self.on_click()
            return True
        return False

    def draw(self):
        color = ToggleButton.TOGGLE_COLOR if self.toggled else Button.BUTTON_COLOR
        GeoDrawer.draw_filled_rectangle(self.x, self.y, self.w, self.h, color)
        self.sprite.draw()


class SelectionButton(ToggleButton):
    def __init__(self, text, toggled=False):
        super().__init__(text, on_click=None, toggled=toggled)

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

    def __init__(self, r, c):
        self.x, self.y, self.w, self.h = (0,) * 4
        self.button_w, self.button_h = (0,) * 2
        self.buttons: List[List[Button]] = [[None for _ in range(c)] for _ in range(r)]
        self.selection_groups = []

    def add_selection_group(self, grp, on_click):
        self.selection_groups.append(SelectionGroup(grp, on_click))

    def selection_group_event(self, s_grp, r, c):
        _r, _c = s_grp.i_to_rc[s_grp.selected]
        if _r == r and _c == c:
            return
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
