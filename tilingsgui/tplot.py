"""[TODO]
"""

from collections import deque
from typing import ClassVar, Deque

from tilings import Tiling

from .graphics import Color, Point, PointPath


class TPlot:
    @staticmethod
    def gridded_perm_initial_locations(gp, gridsz, cellsz):
        colcount = [0] * gridsz[0]
        rowcount = [0] * gridsz[1]
        col = [[] for i in range(gridsz[0])]
        row = [[] for i in range(gridsz[1])]
        locs = PointPath.create_empty()
        for ind in range(len(gp)):
            cx, cy = gp.pos[ind]
            colcount[cx] += 1
            rowcount[cy] += 1
            col[cx].append(ind)
            row[cy].append(gp.patt[ind])
        for r in row:
            r.sort()
        for ind in range(len(gp)):
            val = gp.patt[ind]
            cx, cy = gp.pos[ind]
            locx = cx * cellsz[0] + cellsz[0] * (col[cx].index(ind) + 1) // (
                colcount[cx] + 1
            )
            locy = cy * cellsz[1] + cellsz[1] * (row[cy].index(val) + 1) // (
                rowcount[cy] + 1
            )
            locs.append(Point(locx, locy))
        return locs

    def __init__(self, tiling, w, h):
        self.tiling = tiling
        self.w = w
        self.h = h
        t_w, t_h = self.tiling.dimensions
        self.obstruction_locs = [
            TPlot.gridded_perm_initial_locations(gp, (t_w, t_h), (w // t_w, h // t_h))
            for gp in self.tiling.obstructions
        ]

        self.requirement_locs = [
            [
                TPlot.gridded_perm_initial_locations(
                    gp, (t_w, t_h), (w // t_w, h // t_h)
                )
                for gp in reqlist
            ]
            for reqlist in self.tiling.requirements
        ]

    def resize(self, width, height):
        for obs in self.obstruction_locs:
            for p in obs:
                p.x = p.x / self.w * width
                p.y = p.y / self.h * height
        for reqlist in self.requirement_locs:
            for req in reqlist:
                for j in range(len(req)):
                    xratio = req[j].x / self.w
                    yratio = req[j].y / self.h
                    req[j].x = xratio * width
                    req[j].y = yratio * height
        self.w = width
        self.h = height

    def draw(self):
        for obs in self.obstruction_locs:
            obs.draw(Color.RED)
        for req in self.requirement_locs:
            req.draw(Color.GREEN)


class TPlotManager:
    MAX_DEQUEUE_SIZE: ClassVar[int] = 100

    def __init__(self, width: int, height: int):
        self.undo_deq: Deque[TPlot] = deque()
        self.redo_deq: Deque[TPlot] = deque()
        self.set_dimensions(width, height)
        self.set_mouse_position(0, 0)

        # TODO: REMOVE
        self.undo_deq.append(TPlot(Tiling.from_string("1234_1324"), width, height))

    def set_dimensions(self, width: int, height: int):
        self.w = width
        self.h = height
        if self.undo_deq:
            self.undo_deq[0].resize(width, height)

    def set_mouse_position(self, m_x, m_y):
        self.m_x = m_x
        self.m_y = m_y

    def add(self, drawing: TPlot):
        self.undo_deq.appendleft(drawing)
        self.redo_deq.clear()
        if len(self.undo_deq) > TPlotManager.MAX_DEQUEUE_SIZE:
            self.undo_deq.pop()

    def undo(self):
        if len(self.undo_deq) > 1:
            self.redo_deq.append(self.undo_deq.popleft())
            self.undo_deq[0].resize(self.w, self.h)

    def redo(self):
        if self.redo_deq:
            self.undo_deq.appendleft(self.redo_deq.pop())
            self.undo_deq[0].resize(self.w, self.h)

    def draw(self):
        if self.undo_deq:
            self.undo_deq[0].draw()
