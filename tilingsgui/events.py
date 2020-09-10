"""Event related module.
"""

from typing import Iterable

import pyglet


class Observer:
    """An observer parent class. It handles creating the link between
    the observer and all its dispatchers.
    """

    def __init__(self, dispatchers: Iterable[pyglet.event.EventDispatcher] = ()):
        """Instansiate observer and setup connection wiht dispatchers.

        Args:
            dispatchers (Iterable[pyglet.event.EventDispatcher]): All event dispatchers
            that this observer should listen to. Defaults to an empty tuple.
        """
        self.add_dispatchers(dispatchers)

    def add_dispatcher(self, dispatcher: pyglet.event.EventDispatcher):
        """Add a single dispatcher that this observer should listen to.

        Args:
            dispatcher (pyglet.event.EventDispatcher): A dispatcher
            that this observer should listen to.
        """
        dispatcher.push_handlers(self)

    def add_dispatchers(self, dispatchers: Iterable[pyglet.event.EventDispatcher]):
        """Add multiple dispatchers that this observer should listen to.

        Args:
            dispatchers (Iterable[pyglet.event.EventDispatcher]): Event dispatchers
            that this observer should listen to.
        """
        for dispatcher in dispatchers:
            dispatcher.push_handlers(self)


class CustomEvents:
    """A collection of string constants with names of custom events."""

    ON_PLACEMENT_INPUT = "on_placement_input"
    ON_FETCH_TILING_FOR_EXPORT = "on_fetch_tiling_for_export"
    ON_UNDO = "on_undo"
    ON_REDO = "on_redo"
    ON_ROW_COL_SEPERATION = "on_row_col_seperation"
    ON_OBSTRUCTION_TRANSIVITY = "on_obstruction_transivity"
    ON_BASIS_INPUT = "on_basis_input"
    ON_TILING_JSON_INPUT = "on_tiling_json_input"
    ON_EXPORT = "on_export"
    ON_PRINT_SEQUENCE = "on_print_sequence"
    ON_PRINT_TILING = "on_print_tiling"
    ON_VERIFICATION = "on_verification"
    ON_TIKZ = "on_tikz"
    ON_OBSTRUCTION_INFERRAL = "on_obstruction_inferral"
