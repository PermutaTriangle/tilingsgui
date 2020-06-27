"""Graphical UI components.
"""

from typing import Callable, ClassVar, Dict, List, Optional, Tuple

import pyglet

from .graphics import Color, GeoDrawer

RGB = Tuple[float, float, float]
RGBA = Tuple[float, float, float, float]


class Text:
    """A class for input text.
    """

    _LEFT_PAD: ClassVar[int] = 5

    def __init__(self, init_text: str, font_size: int, color: RGBA) -> None:
        """Create an instance of a user editable text.

        Args:
            init_text (str): The initially set text value.
            font_size (int): The font size for the input field.
            color (Tuple[float, float, float, float]): The font color.
        """

        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.document: pyglet.text.document.UnformattedDocument = (
            pyglet.text.document.UnformattedDocument(init_text)
        )
        self.document.set_style(0, 0, dict(font_size=font_size, color=color))
        self.layout: pyglet.text.layout.IncrementalTextLayout = (
            pyglet.text.layout.IncrementalTextLayout(
                self.document, 0, 0, multiline=False, batch=self.batch
            )
        )
        self.caret: pyglet.text.caret.Caret = pyglet.text.caret.Caret(self.layout)
        self.caret.visible = False

    def position(self, x: float, y: float, w: float, h: float) -> None:
        """Position the component within the viewport.

        Args:
            x (float): The left end of the component.
            y (float): The bottom end of the component.
            w (float): The horizontal length of the component.
            h (float): The vertical length of the component.
        """
        self.layout.x = x + Text._LEFT_PAD
        self.layout.y = y
        self.layout.width = w - Text._LEFT_PAD
        self.layout.height = h

    def set_focus(self) -> None:
        """Set focus on the input text. This is needed to write to it.
        """
        self.document.text = ""
        self.caret.visible = True

    def release_focus(self) -> None:
        """Remove focus from the input text.
        """
        self.caret.visible = False
        self.caret.mark = self.caret.position = 0

    def add_text(self, text: str) -> None:
        """Add text to the current caret position

        Args:
            text (str): The text to add.
        """
        self.caret.on_text(text)

    def has_focus(self) -> bool:
        """Check if input text has focus.

        Returns:
            bool: True iff has focus.
        """
        return self.caret.visible

    def get_current_text(self) -> str:
        """Get the text for the text input.

        Returns:
            str: The current input.
        """
        return self.document.text

    def draw(self) -> None:
        """Draw the text.
        """
        self.batch.draw()

    def move_text(self, motion: int) -> None:
        """Update the caret with events such as home, left, right, delete, etc.

        Args:
            motion (int): The motion event.
        """
        self.caret.on_text_motion(motion)


class TextBox(Text):
    """A class for input text along with a rectangular box around it.
    """

    def __init__(
        self, init_text: str, font_size: int, text_color: RGBA, box_color: RGB,
    ) -> None:
        super().__init__(init_text, font_size, text_color)
        self.vertex_list: pyglet.graphics.vertexdomain.VertexList = self.batch.add(
            4, pyglet.gl.GL_QUADS, None, ("v2f", [0] * 8), ("c3B", box_color * 4),
        )

    def position(self, x: float, y: float, w: float, h: float) -> None:
        super().position(x, y, w, h)
        for i, vertex in enumerate((x, y, x + w, y, x + w, y + h, x, y + h)):
            self.vertex_list.vertices[i] = vertex

    def hit_test(self, x: float, y: float) -> None:
        return (
            self.vertex_list.vertices[0] < x < self.vertex_list.vertices[2]
            and self.vertex_list.vertices[1] < y < self.vertex_list.vertices[5]
        )


class Button:
    BUTTON_COLOR: ClassVar[RGB] = Color.GRAY

    def __init__(
        self, image: str, on_click: Optional[Callable[[], None]] = None
    ) -> None:
        self.sprite: pyglet.sprite.Sprite = (
            pyglet.sprite.Sprite(pyglet.resource.image(image), x=0, y=0)
        )
        self.x: float = 0
        self.y: float = 0
        self.w: float = 0
        self.h: float = 0
        self.on_click: Optional[Callable[[], None]] = on_click

    def hit(self, x: float, y: float) -> bool:
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def click_check(self, x: float, y: float) -> bool:
        if self.hit(x, y):
            if self.on_click is not None:
                self.on_click()
            return True
        return False

    def draw(self) -> None:
        GeoDrawer.draw_rectangle(self.x, self.y, self.w, self.h, Button.BUTTON_COLOR)
        self.sprite.draw()

    def position(self, x: float, y: float, w: float, h: float) -> None:
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

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        toggled: bool = False,
    ) -> None:
        super().__init__(text, on_click)
        self.toggled: bool = toggled

    def click_check(self, x: float, y: float) -> bool:
        if self.hit(x, y):
            if self.on_click is not None:
                self.toggled = not self.toggled
                self.on_click()
            return True
        return False

    def draw(self) -> None:
        color = ToggleButton.TOGGLE_COLOR if self.toggled else Button.BUTTON_COLOR
        GeoDrawer.draw_rectangle(self.x, self.y, self.w, self.h, color)
        self.sprite.draw()


class SelectionButton(ToggleButton):
    def __init__(self, text: str, toggled: bool = False) -> None:
        super().__init__(text, on_click=None, toggled=toggled)

    def click_check(self, x: float, y: float) -> bool:
        if self.hit(x, y):
            self.toggled = True
            return True
        return False


class SelectionGroup:
    def __init__(
        self,
        grp: List[Tuple[int, int]],
        on_click: Optional[Callable[[], None]],
        selected: int = 0,
    ) -> None:
        self.rc_to_i: Dict[Tuple[int, int], int] = (
            {(r, c): i for i, (r, c) in enumerate(grp)}
        )
        self.i_to_rc: List[Tuple[int, int]] = grp
        self.on_click: Optional[Callable[[], None]] = on_click
        self.selected: int = selected

    def __contains__(self, key: Tuple[int, int]) -> bool:
        return key in self.rc_to_i


class ButtonGrid:
    PADDING = 1

    def __init__(self, r: int, c: int) -> None:
        self.x: float = 0
        self.y: float = 0
        self.w: float = 0
        self.h: float = 0
        self.button_w: float = 0
        self.button_h: float = 0
        self.buttons: List[List[Optional[Button]]] = [
            [None for _ in range(c)] for _ in range(r)
        ]
        self.selection_groups: List[SelectionGroup] = []

    def add_selection_group(self, grp, on_click) -> None:
        self.selection_groups.append(SelectionGroup(grp, on_click))

    def selection_group_event(self, s_grp, r, c) -> None:
        _r, _c = s_grp.i_to_rc[s_grp.selected]
        if _r == r and _c == c:
            return
        self.buttons[_r][_c].toggled = not self.buttons[_r][_c].toggled
        s_grp.selected = s_grp.rc_to_i[(r, c)]
        s_grp.on_click(s_grp.selected)

    def resize(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.button_w = w / len(self.buttons[0])
        self.button_h = h / len(self.buttons)
        self.position_btns()

    def add_btn(self, r: int, c: int, btn: Button) -> None:
        self.buttons[r][c] = btn

    def draw(self) -> None:
        for row in self.buttons:
            for button in row:
                if button is not None:
                    button.draw()

    def position_btns(self) -> None:
        for _r, row in enumerate(self.buttons):
            for _c, btn in enumerate(row):
                if btn is not None:
                    self.place_btn_within_grid(btn, _r, _c)

    def place_btn_within_grid(self, btn: Button, r: int, c: int) -> None:
        btn.position(
            self.x + self.button_w * c + ButtonGrid.PADDING,
            self.y + self.button_h * r + ButtonGrid.PADDING,
            self.button_w - 2 * ButtonGrid.PADDING,
            self.button_h - 2 * ButtonGrid.PADDING,
        )

    def click_check(self, x: float, y: float) -> None:
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
