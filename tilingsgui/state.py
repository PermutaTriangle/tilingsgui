"""A global state for the app, in a seperate module.
"""

from typing import Tuple


class MoveState:
    """A collection of states that have to do with draggin points.

    Initial values:
        has_selected_pnt        = False
        selected_point          = tuple()
        point_move_bounds       = tuple()
        move_type               = 0
    """

    def __init__(self) -> None:
        self.has_selected_pnt: bool = False
        self.selected_point: Tuple = tuple()
        self.point_move_bounds: Tuple = tuple()
        self.move_type: int = 0

    def reset(self) -> None:
        """Reset all values to their default values.
        """
        self.has_selected_pnt = False
        self.selected_point = tuple()
        self.point_move_bounds = tuple()
        self.move_type = 0


class GuiState:
    """A collection of various states that are used by multiple components.

    Initial values:
        shading                 = True
        pretty_points           = True
        show_crossing           = True
        show_localized          = True
        highlight_touching_cell = False
        action_selected         = 0
        move_state              = MoveState init's value
    """

    def __init__(self) -> None:
        """Create a state, with all values set to their default.
        """

        self.shading: bool = True
        self.pretty_points: bool = True
        self.show_crossing: bool = True
        self.show_localized: bool = True
        self.highlight_touching_cell: bool = False
        self.action_selected: int = 0
        self.move_state = MoveState()

    def toggle_shading(self) -> None:
        """If shading is on, turn if off and vice versa.
        """
        self.shading = not self.shading

    def toggle_pretty_points(self) -> None:
        """If pretty points is on, turn if off and vice versa.
        """
        self.pretty_points = not self.pretty_points

    def toggle_show_crossing(self) -> None:
        """If show crossing is on, turn if off and vice versa.
        """
        self.show_crossing = not self.show_crossing

    def toggle_show_localized(self) -> None:
        """If show localized is on, turn if off and vice versa.
        """
        self.show_localized = not self.show_localized

    def toggle_highlight_touching_cell(self) -> None:
        """If highlighting is on, turn if off and vice versa.
        """
        self.highlight_touching_cell = not self.highlight_touching_cell

    def set_mouse_click_action(self, idx: int) -> None:
        """Set the chosen action for what the mouse click does.

        Args:
            idx (int): The index of the action chosen.
        """
        self.action_selected = idx
