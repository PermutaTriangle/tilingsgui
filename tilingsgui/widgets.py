import pyglet

from tilingsgui.graphics import Color, GeoDrawer


class Button:
    FONT_SIZE = 10
    LABEL_COLOR = Color.alpha_extend(Color.BLACK)
    BUTTON_COLOR = Color.GRAY

    def __init__(self, text, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = pyglet.text.Label(
            text,
            font_size=Button.FONT_SIZE,
            x=x + w / 2,
            y=y + h / 2,
            font_name="Impact",
            anchor_x="center",
            anchor_y="center",
            color=Button.LABEL_COLOR,
        )

    def hit_test(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def mouse_click(self, x, y):
        if self.hit_test(x, y):
            self.on_click()

    def on_click(self):
        print("click")

    def draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.x, self.y, self.w, self.h, Button.BUTTON_COLOR
        )
        self.label.draw()


class ToggleButton(Button):
    TOGGLE_COLOR = Color.DARK_GRAY

    def __init__(self, text, x, y, w, h):
        super().__init__(text, x, y, w, h)
        self.toggle = False

    def on_click(self):
        self.toggle = not self.toggle
        print("click")

    def draw(self):
        GeoDrawer.draw_filled_rectangle(
            self.x,
            self.y,
            self.w,
            self.h,
            ToggleButton.TOGGLE_COLOR if self.toggle else Button.BUTTON_COLOR,
        )
        self.label.draw()


class SelectButton:
    pass


class SelectButtonGroup:
    pass


class InputBox:
    pass
