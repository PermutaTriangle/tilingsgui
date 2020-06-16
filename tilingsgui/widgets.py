import pyglet

from tilingsgui.graphics import Color, GeoDrawer


class Button:
    FONT_SIZE = 15
    FONT = "Times New Roman"
    LABEL_COLOR = Color.alpha_extend(Color.BLACK)
    BUTTON_COLOR = Color.GRAY

    def __init__(self, text, x=0, y=0, w=0, h=0):
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

    def hit(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def clicked(self, x, y):
        if self.hit(x, y):
            self.on_click()
            return True
        return False

    def on_click(self):
        pass

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
    TOGGLE_COLOR = Color.DARK_GREEN

    def __init__(self, text):
        super().__init__(text)
        self.toggle = False

    def on_click(self):
        self.toggle = not self.toggle

    def draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.x,
            self.y,
            self.w,
            self.h,
            ToggleButton.TOGGLE_COLOR if self.toggle else Button.BUTTON_COLOR,
        )
        self.label.draw()


SelectButton = ToggleButton


class SelectButtonGroup:
    def __init__(self):
        self.buttons = []
        self.selected = -1

    def add_button(self, button):
        self.buttons.append(button)

    def clicked(self, x, y):
        old_selected = self.selected
        for i, button in enumerate(self.buttons):
            if button.clicked(x, y):
                self.selected = i
                if self.selected != old_selected:
                    if old_selected != -1:
                        self.buttons[old_selected].toggle = False
                    return i
                self.buttons[old_selected].toggle = True
                break
        return -1

    def draw(self):
        for btn in self.buttons:
            btn.draw()


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
        # self.position(x, y, width, height)

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
