"""Graphical UI components.
"""

from typing import Callable, ClassVar, Dict, List, Optional, Tuple

import pyglet

from .geometry import Rectangle
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

        self._batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self._document: pyglet.text.document.UnformattedDocument = (
            pyglet.text.document.UnformattedDocument(init_text)
        )
        self._document.set_style(0, 0, dict(font_size=font_size, color=color))
        self._layout: pyglet.text.layout.IncrementalTextLayout = (
            pyglet.text.layout.IncrementalTextLayout(
                self._document, 0, 0, multiline=False, batch=self._batch
            )
        )
        self._caret: pyglet.text.caret.Caret = pyglet.text.caret.Caret(self._layout)
        self._caret.visible = False

    def position(self, x: float, y: float, w: float, h: float) -> None:
        """Position the component within the viewport.

        Args:
            x (float): The left end of the component.
            y (float): The bottom end of the component.
            w (float): The horizontal length of the component.
            h (float): The vertical length of the component.
        """
        self._layout.x = x + Text._LEFT_PAD
        self._layout.y = y
        self._layout.width = w - Text._LEFT_PAD
        self._layout.height = h

    def set_focus(self) -> None:
        """Set focus on the input text. This is needed to write to it.
        """
        self._document.text = ""
        self._caret.visible = True

    def release_focus(self) -> None:
        """Remove focus from the input text.
        """
        self._caret.visible = False
        self._caret.mark = self._caret.position = 0

    def add_text(self, text: str) -> None:
        """Add text to the current caret position

        Args:
            text (str): The text to add.
        """
        self._caret.on_text(text)

    def has_focus(self) -> bool:
        """Check if input text has focus.

        Returns:
            bool: True iff has focus.
        """
        return self._caret.visible

    def get_current_text(self) -> str:
        """Get the text for the text input.

        Returns:
            str: The current input.
        """
        return self._document.text

    def draw(self) -> None:
        """Draw the text.
        """
        self._batch.draw()

    def move_text(self, motion: int) -> None:
        """Update the caret with events such as home, left, right, delete, etc.

        Args:
            motion (int): The motion event.
        """
        self._caret.on_text_motion(motion)


class TextBox(Text):
    """A class for input text along with a rectangular box around it.
    """

    def __init__(
        self, init_text: str, font_size: int, text_color: RGBA, box_color: RGB,
    ) -> None:
        """Create an instance of a text box.

        Args:
            init_text (str): The initial text displayed.
            font_size (int): The font size of the displayed text.
            text_color (Tuple[float, float, float, float]): The rgba color of the text.
            box_color (Tuple[float, float, float]): The rgb color of the box.
        """
        super().__init__(init_text, font_size, text_color)
        self._vertex_list: pyglet.graphics.vertexdomain.VertexList = self._batch.add(
            4, pyglet.gl.GL_QUADS, None, ("v2f", [0] * 8), ("c3B", box_color * 4),
        )

    def position(self, x: float, y: float, w: float, h: float) -> None:
        """Position the component within the viewport.

        Args:
            x (float): The left end of the component.
            y (float): The bottom end of the component.
            w (float): The horizontal length of the component.
            h (float): The vertical length of the component.
        """
        super().position(x, y, w, h)
        for i, vertex in enumerate((x, y, x + w, y, x + w, y + h, x, y + h)):
            self._vertex_list.vertices[i] = vertex

    def hit_test(self, x: float, y: float) -> bool:
        """Is the point (x,y) inside the rectangle that the text box forms.

        Args:
            x (float): The x coordinate of the point.
            y (float): The y coordinate of the point.

        Returns:
            [type]: True iff inside.
        """
        return (
            self._vertex_list.vertices[0] < x < self._vertex_list.vertices[2]
            and self._vertex_list.vertices[1] < y < self._vertex_list.vertices[5]
        )


class Button:
    """A clickable rectangular GUI component.
    """

    _BUTTON_COLOR: ClassVar[RGB] = Color.GRAY

    def __init__(
        self, image: str, on_click: Optional[Callable[[], None]] = None
    ) -> None:
        """Create an instance of a clickable button.

        Args:
            image (str): The name of the image file to use as a symbol for the button.
            on_click (Optional[Callable[[], None]], optional): A callback function that
            is called in click_check if the button was clicked. Defaults to None.
        """
        self._sprite: pyglet.sprite.Sprite = (
            pyglet.sprite.Sprite(pyglet.resource.image(image), x=0, y=0)
        )
        self._x: float = 0
        self._y: float = 0
        self._w: float = 0
        self._h: float = 0
        self._on_click: Optional[Callable[[], None]] = on_click

    def click_check(self, x: float, y: float) -> bool:
        """Checks if the button has been clicked and calls the on_click function
        if so given that one is defined.

        Args:
            x (float): The click x coordinate.
            y (float): the click y coordinate.

        Returns:
            bool: True if clicked.
        """
        if self._hit_test(x, y):
            if self._on_click is not None:
                self._on_click()
            return True
        return False

    def draw(self) -> None:
        """Draw the button.
        """
        GeoDrawer.draw_rectangle(
            self._x, self._y, self._w, self._h, Button._BUTTON_COLOR
        )
        self._sprite.draw()

    def position(self, x: float, y: float, w: float, h: float) -> None:
        """Position the button within the viewport.

        Args:
            x (float): The left end of the button.
            y (float): The bottom end of the button.
            w (float): The horizontal length of the button.
            h (float): The vertical length of the button.
        """
        self._x, self._y, self._w, self._h = x, y, w, h
        dim = min(w, h)
        if dim > 0:
            self._sprite.scale *= dim / self._sprite.width
            self._sprite.x = x + self._w / 2 - self._sprite.width / 2
            self._sprite.y = y + self._h / 2 - self._sprite.height / 2

    def _hit_test(self, x: float, y: float) -> bool:
        """Check if the (x,y) coordinate is within the rectangular bounds of the button.

        Args:
            x (float): The x coordinate of the collision point.
            y (float): The y coordinate of the collision point.

        Returns:
            bool: True if point is within the button.
        """
        return self._x < x < self._x + self._w and self._y < y < self._y + self._h


class ToggleButton(Button):
    """A button that is either on or off.
    """

    _TOGGLE_COLOR: ClassVar[RGB] = Color.DARK_OLIVE_GREEN

    def __init__(
        self,
        image: str,
        on_click: Optional[Callable[[], None]] = None,
        toggled: bool = False,
    ) -> None:
        """Create an instance of a toggleable button.

        Args:
            image (str): The name of the image file to use as a symbol for the button.
            on_click (Optional[Callable[[], None]], optional):  A callback function that
            is called in click_check if the button was clicked. Defaults to None.
            toggled (bool, optional): Start as toggled? Defaults to False.
        """
        super().__init__(image, on_click)
        self._toggled: bool = toggled

    def click_check(self, x: float, y: float) -> bool:
        """Checks if the button has been clicked and calls the on_click function
        if so given that one is defined and handles toggling.

        Args:
            x (float): The click x coordinate.
            y (float): the click y coordinate.

        Returns:
            bool: True if clicked.
        """
        if self._hit_test(x, y):
            if self._on_click is not None:
                self.toggle()
                self._on_click()
            return True
        return False

    def draw(self) -> None:
        """Draw the button.
        """
        color = ToggleButton._TOGGLE_COLOR if self._toggled else Button._BUTTON_COLOR
        GeoDrawer.draw_rectangle(self._x, self._y, self._w, self._h, color)
        self._sprite.draw()

    def toggle(self) -> None:
        """If on, turn off and vice versa.
        """
        self._toggled = not self._toggled


class SelectionButton(ToggleButton):
    """A button that belongs to a group of buttons and only one can be selected.
    """

    def __init__(self, image: str, selected: bool = False) -> None:
        """Create an instance of a selectable button.

        Args:
            image (str): The name of the image file to use as a symbol for the button.
            selected (bool, optional): Is it selected initially?. Defaults to False.
        """
        super().__init__(image, on_click=None, toggled=selected)

    def click_check(self, x: float, y: float) -> bool:
        """Checks if the button has been clicked and if so, marks it as selected.

        Args:
            x (float): The click x coordinate.
            y (float): the click y coordinate.

        Returns:
            bool: True if clicked.
        """
        if self._hit_test(x, y):
            self._toggled = True
            return True
        return False


class SelectionGroup:
    """A grouping of selection buttons.
    """

    def __init__(
        self,
        grp: List[Tuple[int, int]],
        on_click: Optional[Callable[[int], None]],
        selected: int = 0,
    ) -> None:
        """Create a selection group.

        Args:
            grp (List[Tuple[int, int]]): The postion of the buttons within a grid.
            on_click (Optional[Callable[[], None]]): A click callback for the group.
            selected (int, optional): The index of the button initially selected.
            Defaults to 0.
        """
        self._rc_to_i: Dict[Tuple[int, int], int] = (
            {(r, c): i for i, (r, c) in enumerate(grp)}
        )
        self._i_to_rc: List[Tuple[int, int]] = grp
        self._on_click: Optional[Callable[[int], None]] = on_click
        self._selected: int = selected

    def click(self) -> None:
        """Call on_click for the currenty selected button.
        """
        if self._on_click is not None:
            self._on_click(self._selected)

    def get_row_col_of_selected(self) -> Tuple[int, int]:
        """Get the row and column within the grid of the currently selected button.

        Returns:
            Tuple[int, int]: The (row, column) as a tuple.
        """
        return self._i_to_rc[self._selected]

    def select(self, r: int, c: int) -> None:
        """Select a button within a selection group.

        Args:
            r (int): The row within the grid of the button to select.
            c (int): The column within the grid of the button to select.
        """
        self._selected = self._rc_to_i[(r, c)]

    def __contains__(self, key: Tuple[int, int]) -> bool:
        """Does a grid position belong to a selection group?

        Args:
            key (Tuple[int, int]): A grid position.

        Returns:
            bool: True iff grid positions belongs to selection group.
        """
        return key in self._rc_to_i


class ButtonGrid:
    """A positional object to place and group buttons together.
    """

    _PADDING: ClassVar[int] = 1

    def __init__(self, r: int, c: int) -> None:
        """Create a button grid with r rows and c columns.

        Args:
            r (int): The number of rows.
            c (int): The number of columns.
        """
        self.rect: Rectangle = Rectangle(0, 0, 0, 0)
        self.button_w: float = 0
        self.button_h: float = 0
        self.buttons: List[List[Optional[Button]]] = [
            [None for _ in range(c)] for _ in range(r)
        ]
        self.selection_groups: List[SelectionGroup] = []

    def add_selection_group(
        self, grp: List[Tuple[int, int]], on_click: Optional[Callable[[int], None]]
    ) -> None:
        """Add a selection group to the grid. It is the caller's responsibility to
        make sure buttons aren't in multiple groups and are of the appropriate type.

        Args:
            grp (List[Tuple[int, int]]): A list of coordinates within the grid system.
            on_click (Optional[Callable[[int], None]]): A callback function for a
            click event within the selection group. It takes the index of the selected
            button as a parameter.
        """
        self.selection_groups.append(SelectionGroup(grp, on_click))

    def position(self, x: float, y: float, w: float, h: float) -> None:
        """Position the grid within the viewport.

        Args:
            x (float): The left end of the grid.
            y (float): The bottom end of the grid.
            w (float): The horizontal length of the grid.
            h (float): The vertical length of the grid.
        """
        self.rect.x, self.rect.y, self.rect.h, self.rect.h = x, y, w, h
        self.button_w, self.button_h = w / len(self.buttons[0]), h / len(self.buttons)
        self._position_btns()

    def add_btn(self, r: int, c: int, btn: Button) -> None:
        """Add a button to the button grid by position within it.

        Args:
            r (int): The row of the button to add.
            c (int): The column of the button to add.
            btn (Button): The button to add.
        """
        self.buttons[r][c] = btn

    def draw(self) -> None:
        """Draw the button grid and all its buttons.
        """
        for row in self.buttons:
            for button in row:
                if button is not None:
                    button.draw()

    def click_check(self, x: float, y: float) -> None:
        """Check if the click coordinate (x, y) is within the grid and if so,
        set in motion the events that should follow.

        Args:
            x (float): The x coordinate of a click.
            y (float): The y coordinate of a click.
        """
        for r, row in enumerate(self.buttons):
            for c, btn in enumerate(row):
                if btn is None:
                    continue
                if btn.click_check(x, y):
                    # If btn was clicked, look for selection groups that it belongs to
                    for s_grp in self.selection_groups:
                        if (r, c) in s_grp:
                            self._selection_group_event(s_grp, r, c)
                            # We go by the assumption that no button belongs to multiple
                            # selection groups so we stop if one is found.
                            break
                    return

    def _position_btns(self) -> None:
        """Position all buttons within the grid.
        """
        for _r, row in enumerate(self.buttons):
            for _c, btn in enumerate(row):
                if btn is not None:
                    self._place_btn_within_grid(btn, _r, _c)

    def _place_btn_within_grid(self, btn: Button, r: int, c: int) -> None:
        """Position a specific button within the grid given its position
        in its row-column coordinates.

        Args:
            btn (Button): The button to position.
            r (int): The button's row position within the grid.
            c (int): The button's column position within the grid.
        """
        btn.position(
            self.rect.x + self.button_w * c + ButtonGrid._PADDING,
            self.rect.y + self.button_h * r + ButtonGrid._PADDING,
            self.button_w - 2 * ButtonGrid._PADDING,
            self.button_h - 2 * ButtonGrid._PADDING,
        )

    def _selection_group_event(self, s_grp: SelectionGroup, r: int, c: int) -> None:
        """Called when button in position (r,c) within the grid was clicked and
        he belongs to the selection group s_grp.

        Args:
            s_grp (SelectionGroup): The group that the clicked button belongs to.
            r (int): The row position of the clicked button.
            c (int): The column position of the clicked button.
        """
        _r, _c = s_grp.get_row_col_of_selected()
        if _r == r and _c == c:
            return
        btn = self.buttons[_r][_c]
        # Should always be the case but mypy was angry
        if isinstance(btn, SelectionButton):
            btn.toggle()
            s_grp.select(r, c)
            s_grp.click()
