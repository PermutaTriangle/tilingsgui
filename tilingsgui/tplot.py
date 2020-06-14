"""[TODO]
"""

from collections import deque
from typing import ClassVar, Deque, Tuple

from permuta import Perm
from permuta.misc import DIR_NORTH
from tilings import Tiling

from .geo import Point
from .graphics import Color, GeoDrawer
from .interface import Drawable, EventListener


class TPlotSettings:
    def __init__(self):
        self.shading: bool = True
        self.pretty_points: bool = True
        self.show_crossing: bool = True
        self.show_localized: bool = True
        self.highlight_touching_cell: bool = False


class TPlot:
    OBSTRUCTION_COLOR: ClassVar[Tuple[float, float, float]] = Color.RED
    REQUIREMENT_COLOR: ClassVar[Tuple[float, float, float]] = Color.GREEN

    @staticmethod
    def gridded_perm_initial_locations(gp, gridsz, cellsz):
        colcount = [0] * gridsz[0]
        rowcount = [0] * gridsz[1]
        col = [[] for i in range(gridsz[0])]
        row = [[] for i in range(gridsz[1])]
        locs = []
        for ind in range(len(gp)):
            c_x, c_y = gp.pos[ind]
            colcount[c_x] += 1
            rowcount[c_y] += 1
            col[c_x].append(ind)
            row[c_y].append(gp.patt[ind])
        for r in row:
            r.sort()
        for ind in range(len(gp)):
            val = gp.patt[ind]
            c_x, c_y = gp.pos[ind]
            locx = c_x * cellsz[0] + cellsz[0] * (col[c_x].index(ind) + 1) // (
                colcount[c_x] + 1
            )
            locy = c_y * cellsz[1] + cellsz[1] * (row[c_y].index(val) + 1) // (
                rowcount[c_y] + 1
            )
            locs.append(Point(locx, locy))
        return locs

    def __init__(self, tiling, w, h):
        self.tiling = tiling
        self.w = w
        self.h = h
        t_w, t_h = self.tiling.dimensions
        self.obstruction_locs = [
            TPlot.gridded_perm_initial_locations(gp, (t_w, t_h), (w / t_w, h / t_h))
            for gp in self.tiling.obstructions
        ]

        self.requirement_locs = [
            [
                TPlot.gridded_perm_initial_locations(gp, (t_w, t_h), (w / t_w, h / t_h))
                for gp in reqlist
            ]
            for reqlist in self.tiling.requirements
        ]

    def resize(self, width, height):
        for obs in self.obstruction_locs:
            for pnt in obs:
                pnt.x = pnt.x / self.w * width
                pnt.y = pnt.y / self.h * height
        for reqlist in self.requirement_locs:
            for req in reqlist:
                for pnt in req:
                    pnt.x = pnt.x / self.w * width
                    pnt.y = pnt.y / self.h * height
        self.w = width
        self.h = height

    def cell_to_rect(self, c):
        cx, cy = c
        tw, th = self.tiling.dimensions
        cw, ch = self.w / tw, self.h / th
        return cx * cw, cy * ch, cw, ch

    def draw_shaded_cells(self):
        for c in self.tiling.empty_cells:
            GeoDrawer.draw_filled_rectangle(*self.cell_to_rect(c), Color.GRAY)

    def draw_point_cells(self):
        for c in self.tiling.point_cells:
            x, y, w, h = self.cell_to_rect(c)
            GeoDrawer.draw_circle(x + w / 2, y + h / 2, 10, Color.BLACK)

    def get_cell(self, mpos: Point):
        tw, th = self.tiling.dimensions
        cw, ch = self.w / tw, self.h / th
        mx, my = mpos.x, mpos.y
        cx, cy = int(mx / cw), int(my / ch)
        return (cx, cy)

    def get_point_obs_index(self, mpos: Point):
        for j, loc in enumerate(self.obstruction_locs):
            for k, v in enumerate(loc):
                if mpos.dist_squared_to(v) <= 100:
                    return (j, k)

    def get_point_req_index(self, mpos: Point):
        for i, reqlist in enumerate(self.requirement_locs):
            for j, loc in enumerate(reqlist):
                for k, v in enumerate(loc):
                    if mpos.dist_squared_to(v) <= 100:
                        return (i, j, k)

    def draw(self, settings: TPlotSettings, mpos: Point):
        highlight_col = Color.BLACK
        tw, th = self.tiling.dimensions
        hover_cell = self.get_cell(mpos)
        hover_index = self.get_point_req_index(mpos)
        if settings.shading:
            self.draw_shaded_cells()
        if settings.pretty_points:
            self.draw_point_cells()
        for i in range(tw):
            x = self.w * i / tw
            GeoDrawer.draw_line_segment(x, self.h, x, 0, Color.BLACK)
        for i in range(th):
            y = self.h * i / th
            GeoDrawer.draw_line_segment(0, y, self.w, y, Color.BLACK)
        for i, loc in enumerate(self.obstruction_locs):
            if settings.shading and self.tiling.obstructions[i].is_point_perm():
                continue
            if settings.pretty_points and all(
                p in self.tiling.point_cells for p in self.tiling.obstructions[i].pos
            ):
                continue
            col = TPlot.OBSTRUCTION_COLOR
            if settings.highlight_touching_cell and any(
                p == hover_cell for p in self.tiling.obstructions[i].pos
            ):
                col = highlight_col
            localized = self.tiling.obstructions[i].is_localized()
            if (localized and settings.show_localized) or (
                not localized and settings.show_crossing
            ):
                GeoDrawer.draw_point_path(loc, col, 5)
        for i, reqlist in enumerate(self.requirement_locs):
            if settings.pretty_points and any(
                p in self.tiling.point_cells
                for req in self.tiling.requirements[i]
                for p in req.pos
            ):
                continue
            col = (
                highlight_col
                if hover_index is not None and i == hover_index[0]
                else TPlot.REQUIREMENT_COLOR
            )
            for j, loc in enumerate(reqlist):
                localized = self.tiling.requirements[i][j].is_localized()
                if (localized and settings.show_localized) or (
                    not localized and settings.show_crossing
                ):
                    GeoDrawer.draw_point_path(loc, col, 5)


class TPlotManager(Drawable, EventListener):
    MAX_DEQUEUE_SIZE: ClassVar[int] = 100

    def __init__(self, width: int, height: int):
        self.undo_deq: Deque[TPlot] = deque()
        self.redo_deq: Deque[TPlot] = deque()
        self.set_dimensions(width, height)
        self.mouse_pos = Point(0, 0)

        self.settings = TPlotSettings()

        # TODO: REMOVE
        test_tiling = Tiling.from_string("1234_1324").add_single_cell_requirement(
            Perm((0,)), (0, 0)
        )
        test_tiling = test_tiling.place_point_of_gridded_permutation(
            test_tiling.requirements[0][0], 0, DIR_NORTH
        )
        self.undo_deq.append(TPlot(test_tiling, width, height))

    def set_dimensions(self, width: int, height: int):
        self.w = width
        self.h = height
        if self.undo_deq:
            self.undo_deq[0].resize(width, height)

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
            self.undo_deq[0].draw(self.settings, self.mouse_pos)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos.x = x
        self.mouse_pos.y = y

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_resize(self, width, height):
        self.set_dimensions(width, height)
