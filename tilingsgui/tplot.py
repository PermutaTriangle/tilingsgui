
from collections import deque
from typing import ClassVar, Deque

from tilings import Tiling


class TilingDrawing:
    def __init__(self, tiling):
        pass
        print(Tiling.from_string("1234"))


# Rename to something not so similar... TilingDrawingManager?
class TilingDrawings:
    MAX_DEQUEUE_SIZE: ClassVar[int] = 100

    def __init__(self, width: int, height: int):
        self.undo_deq: Deque[TilingDrawing] = deque()
        self.redo_deq: Deque[TilingDrawing] = deque()
        self.set_dimensions(width, height)
        self.set_mouse_position(0, 0)

    def set_dimensions(self, width: int, height: int):
        self.w = width
        self.h = height

    def set_mouse_position(self, m_x, m_y):
        self.m_x = m_x
        self.m_y = m_y

    def add(self, drawing: TilingDrawing):
        self.undo_deq.appendleft(drawing)
        self.redo_deq.clear()
        if len(self.undo_deq) > TilingDrawings.MAX_DEQUEUE_SIZE:
            self.undo_deq.pop()

    def undo(self):
        if len(self.undo_deq) > 1:
            self.redo_deq.append(self.undo_deq.popleft())

    def redo(self):
        if self.redo_deq:
            self.undo_deq.appendleft(self.redo_deq.pop())

    def draw_current(self):
        pass

    def get_current(self):
        pass
