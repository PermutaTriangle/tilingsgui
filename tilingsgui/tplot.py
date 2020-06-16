"""[TODO]
"""

from collections import deque
from typing import ClassVar, Deque, Tuple

from tilings import Tiling
from tilingsgui.geo import Point
from tilingsgui.graphics import Color, GeoDrawer
from tilingsgui.state import GuiState


class TPlot:
    OBSTRUCTION_COLOR: ClassVar[Tuple[float, float, float]] = Color.RED
    REQUIREMENT_COLOR: ClassVar[Tuple[float, float, float]] = Color.GREEN
    HIGHLIGHT_COLOR: ClassVar[Tuple[float, float, float]] = Color.BLACK

    @staticmethod
    def _col_row_and_count(gp, gridsz):
        colcount = [0] * gridsz[0]
        rowcount = [0] * gridsz[1]
        col = [[] for i in range(gridsz[0])]
        row = [[] for i in range(gridsz[1])]
        for ind, ((c_x, c_y), val) in enumerate(zip(gp.pos, gp.patt)):
            colcount[c_x] += 1
            rowcount[c_y] += 1
            col[c_x].append(ind)
            row[c_y].append(val)
        for r in row:
            r.sort()
        return colcount, rowcount, col, row

    @staticmethod
    def gridded_perm_initial_locations(gp, gridsz, cellsz):
        colcount, rowcount, col, row = TPlot._col_row_and_count(gp, gridsz)
        locs = [
            Point(
                cellsz[0] * (c_x + (col[c_x].index(ind) + 1) / (colcount[c_x] + 1)),
                cellsz[1] * (c_y + (row[c_y].index(val) + 1) / (rowcount[c_y] + 1)),
            )
            for ind, ((c_x, c_y), val) in enumerate(zip(gp.pos, gp.patt))
        ]
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

    def draw(self, state: GuiState, mpos: Point):
        if any(len(obs) == 0 for obs in self.tiling.obstructions):
            GeoDrawer.draw_filled_rectangle(0, 0, self.w, self.h, Color.GRAY)
        else:
            if state.shading:
                self._draw_shaded_cells()
            if state.pretty_points:
                self._draw_point_cells()
            self._draw_grid()
            self._draw_obstructions(state, mpos)
            self._draw_requirements(state, mpos)

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

    def _cell_to_rect(self, c_x, c_y):
        t_w, t_h = self.tiling.dimensions
        c_w, c_h = self.w / t_w, self.h / t_h
        return c_x * c_w, c_y * c_h, c_w, c_h

    def _draw_shaded_cells(self):
        for c_x, c_y in self.tiling.empty_cells:
            GeoDrawer.draw_filled_rectangle(*self._cell_to_rect(c_x, c_y), Color.GRAY)

    def _draw_point_cells(self):
        for c_x, c_y in self.tiling.point_cells:
            x, y, w, h = self._cell_to_rect(c_x, c_y)
            GeoDrawer.draw_circle(x + w / 2, y + h / 2, 10, Color.BLACK)

    def _get_cell(self, mpos: Point):
        t_w, t_h = self.tiling.dimensions
        c_w, c_h = self.w / t_w, self.h / t_h
        c_x, c_y = int(mpos.x / c_w), int(mpos.y / c_h)
        return c_x, c_y

    def _get_point_obs_index(self, mpos: Point):
        for j, loc in enumerate(self.obstruction_locs):
            for k, pnt in enumerate(loc):
                if mpos.dist_squared_to(pnt) <= 100:
                    return j, k

    def _get_point_req_index(self, mpos: Point):
        for i, reqlist in enumerate(self.requirement_locs):
            for j, loc in enumerate(reqlist):
                for k, pnt in enumerate(loc):
                    if mpos.dist_squared_to(pnt) <= 100:
                        return i, j, k

    def _draw_obstructions(self, state: GuiState, mpos: Point):
        hover_cell = self._get_cell(mpos)
        for obs, loc in zip(self.tiling.obstructions, self.obstruction_locs):
            if (state.shading and obs.is_point_perm()) or (
                state.pretty_points
                and all(p in self.tiling.point_cells for p in obs.pos)
            ):
                continue

            col = (
                TPlot.HIGHLIGHT_COLOR
                if state.highlight_touching_cell
                and any(p == hover_cell for p in obs.pos)
                else TPlot.OBSTRUCTION_COLOR
            )
            localized = obs.is_localized()
            if (localized and state.show_localized) or (
                not localized and state.show_crossing
            ):
                GeoDrawer.draw_point_path(loc, col, 5)

    def _draw_requirements(self, state: GuiState, mpos: Point):
        hover_index = self._get_point_req_index(mpos)
        for i, reqlist in enumerate(self.requirement_locs):
            if state.pretty_points and any(
                p in self.tiling.point_cells
                for req in self.tiling.requirements[i]
                for p in req.pos
            ):
                continue
            col = (
                TPlot.HIGHLIGHT_COLOR
                if hover_index is not None and i == hover_index[0]
                else TPlot.REQUIREMENT_COLOR
            )

            for j, loc in enumerate(reqlist):
                localized = self.tiling.requirements[i][j].is_localized()
                if (localized and state.show_localized) or (
                    not localized and state.show_crossing
                ):
                    GeoDrawer.draw_point_path(loc, col, 5)

    def _draw_grid(self):
        t_w, t_h = self.tiling.dimensions
        for i in range(t_w):
            x = self.w * i / t_w
            GeoDrawer.draw_line_segment(x, self.h, x, 0, Color.BLACK)
        for i in range(t_h):
            y = self.h * i / t_h
            GeoDrawer.draw_line_segment(0, y, self.w, y, Color.BLACK)


class TPlotManager:
    MAX_DEQUEUE_SIZE: ClassVar[int] = 100

    def __init__(self, width: int, height: int, state: GuiState):
        self.undo_deq: Deque[TPlot] = deque()
        self.redo_deq: Deque[TPlot] = deque()
        self.set_dimensions(width, height)
        self.mouse_pos = Point(0, 0)

        self.state = state

        # TODO: REMOVE
        """test_tiling = Tiling.from_string("1234_1324").add_single_cell_requirement(
            Perm((0,)), (0, 0)
        )
        test_tiling = test_tiling.place_point_of_gridded_permutation(
            test_tiling.requirements[0][0], 0, DIR_NORTH
        )
        self.undo_deq.append(TPlot(test_tiling, width, height))"""

    def set_dimensions(self, width: int, height: int):
        self.w = width
        self.h = height
        if self.undo_deq:
            self.undo_deq[0].resize(width, height)

    def add_from_string(self, string):
        self.add(TPlot(Tiling.from_string(string), self.w, self.h))

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
            self.undo_deq[0].draw(self.state, self.mouse_pos)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos.x = x
        self.mouse_pos.y = y

    def on_resize(self, width, height):
        self.set_dimensions(width, height)
