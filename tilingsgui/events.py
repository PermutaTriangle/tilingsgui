"""Event related module.
"""

from typing import Iterable

import pyglet


class Observer:
    """An observer parent class. It handles creating the link between
    the observer and all its dispatchers.
    """

    def __init__(self, dispatchers: Iterable[pyglet.event.EventDispatcher]):
        """Instansiate observer and setup connection wiht dispatchers.

        Args:
            dispatchers (Iterable[pyglet.event.EventDispatcher]): All event dispatchers
            that this observer should listen to.
        """
        for dispatcher in dispatchers:
            dispatcher.push_handlers(self)
