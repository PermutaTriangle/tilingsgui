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


class ToggleButton(Button):
    TOGGLE_COLOR = Color.DARK_GREEN

    def __init__(self, text, x, y, w, h):
        super().__init__(text, x, y, w, h)
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


class InputBox:
    pass
