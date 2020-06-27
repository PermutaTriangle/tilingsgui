"""[TODO]
"""

from collections import Counter, deque
from random import uniform
from typing import ClassVar, Deque, Tuple

import pyglet

from permuta import Perm
from permuta.misc import DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST
from tilings import Tiling
from tilings.algorithms import Factor, FactorWithInterleaving
from tilings.exception import InvalidOperationError
from tilings.strategies import (
    BasicVerificationStrategy,
    DatabaseVerificationStrategy,
    ElementaryVerificationStrategy,
    LocallyFactorableVerificationStrategy,
    LocalVerificationStrategy,
    MonotoneTreeVerificationStrategy,
    OneByOneVerificationStrategy,
)

from .events import CustomEvents, Observer
from .geometry import Point
from .graphics import Color, GeoDrawer
from .state import GuiState
from .utils import clamp


class TPlot:
    OBSTRUCTION_COLOR: ClassVar[Tuple[float, float, float]] = Color.RED
    REQUIREMENT_COLOR: ClassVar[Tuple[float, float, float]] = Color.BLUE
    HIGHLIGHT_COLOR: ClassVar[Tuple[float, float, float]] = Color.ORANGE
    FUZZYNESS = 0.25  # Should be in (0,0.5)

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
                cellsz[0]
                * (
                    c_x
                    + (
                        col[c_x].index(ind)
                        + 1
                        + uniform(-TPlot.FUZZYNESS, TPlot.FUZZYNESS)
                    )
                    / (colcount[c_x] + 1)
                ),
                cellsz[1]
                * (
                    c_y
                    + (
                        row[c_y].index(val)
                        + 1
                        + uniform(-TPlot.FUZZYNESS, TPlot.FUZZYNESS)
                    )
                    / (rowcount[c_y] + 1)
                ),
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
            GeoDrawer.draw_rectangle(0, 0, self.w, self.h, Color.GRAY)
        else:
            if state.shading:
                self._draw_shaded_cells()
            # if state.pretty_points:
            #    self._draw_point_cells()
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
            GeoDrawer.draw_rectangle(*self._cell_to_rect(c_x, c_y), Color.GRAY)

    """def _draw_point_cells(self):
        point_cells_with_point_perm_req = {
            req.pos[0]
            for req_lis in self.tiling.requirements
            for req in req_lis
            if req.is_point_perm()
        }.intersection(self.tiling.point_cells)

        for c_x, c_y in point_cells_with_point_perm_req:
            x, y, w, h = self._cell_to_rect(c_x, c_y)
            GeoDrawer.draw_circle(x + w / 2, y + h / 2, 10, Color.BLACK)"""

    def get_cell(self, mpos: Point):
        t_w, t_h = self.tiling.dimensions
        c_w, c_h = self.w / t_w, self.h / t_h
        c_x, c_y = int(mpos.x / c_w), int(mpos.y / c_h)
        return c_x, c_y

    def get_point_obs_index(self, mpos: Point):
        for j, loc in enumerate(self.obstruction_locs):
            for k, pnt in enumerate(loc):
                if mpos.dist_squared_to(pnt) <= 100:
                    return j, k

    def get_point_req_index(self, mpos: Point):
        for i, reqlist in enumerate(self.requirement_locs):
            for j, loc in enumerate(reqlist):
                for k, pnt in enumerate(loc):
                    if mpos.dist_squared_to(pnt) <= 100:
                        return i, j, k

    def _draw_obstructions(self, state: GuiState, mpos: Point):
        # TODO: create once, re-use ... pass through drawing functions
        # look for more such optimizations... when done...
        point_cells_with_point_perm_req = self.tiling.point_cells.intersection(
            {
                req.pos[0]
                for req_lis in self.tiling.requirements
                for req in req_lis
                if len(req) == 1
            }
        )
        hover_cell = self.get_cell(mpos)
        for obs, loc in zip(self.tiling.obstructions, self.obstruction_locs):
            if (state.shading and obs.is_point_perm()) or (
                state.pretty_points
                and all(p in point_cells_with_point_perm_req for p in obs.pos)
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
        hover_index = self.get_point_req_index(mpos)
        for i, reqlist in enumerate(self.requirement_locs):
            if (
                len(reqlist[0]) == 1
                and state.pretty_points
                and any(
                    p in self.tiling.point_cells
                    for req in self.tiling.requirements[i]
                    for p in req.pos
                )
            ):
                pnt = reqlist[0][0]
                GeoDrawer.draw_circle(pnt.x, pnt.y, 10, Color.BLACK)
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


"""
###############################
###############################
###############################
###############################
###############################
###############################
###############################
###############################
###############################
###############################
###############################
###############################
###############################
"""


class TPlotManager(pyglet.event.EventDispatcher, Observer):
    MAX_DEQUEUE_SIZE: ClassVar[int] = 100
    MAX_SEQUENCE_SIZE = 7

    def __init__(self, width: int, height: int, state: GuiState, dispatchers):
        Observer.__init__(self, dispatchers)
        self.undo_deq: Deque[TPlot] = deque()
        self.redo_deq: Deque[TPlot] = deque()
        self.position(width, height)
        self.mouse_pos = Point(0, 0)
        self.custom_placement: Perm = Perm((0, 1))
        self.state = state

    # Handlers

    def on_fetch_tiling_for_export(self):
        if not self.empty():
            self.dispatch_event(
                CustomEvents.ON_EXPORT, self.current().tiling.to_jsonable()
            )

    def on_basis_input(self, basis):
        self.add(TPlot(Tiling.from_string(basis), self.w, self.h))

    def on_tiling_json_input(self, basis):
        self.add(TPlot(basis, self.w, self.h))

    def on_placement_input(self, perm):
        self.custom_placement = Perm.to_standard(perm)

    def on_undo(self):
        if self.has_older():
            self.redo_deq.append(self.undo_deq.popleft())
            self.current().resize(self.w, self.h)

    def on_redo(self):
        if self.redo_deq:
            self.undo_deq.appendleft(self.redo_deq.pop())
            self.undo_deq[0].resize(self.w, self.h)

    def on_draw(self):
        if self.undo_deq:
            self.undo_deq[0].draw(self.state, self.mouse_pos)

    def add(self, drawing: TPlot):
        self.undo_deq.appendleft(drawing)
        self.redo_deq.clear()
        if len(self.undo_deq) > TPlotManager.MAX_DEQUEUE_SIZE:
            self.undo_deq.pop()

    def empty(self):
        return not self

    def has_older(self):
        return len(self.undo_deq) > 1

    def __bool__(self):
        return bool(self.undo_deq)

    def current(self):
        return self.undo_deq[0]

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos.x = x
        self.mouse_pos.y = y

    def position(self, width, height):
        self.w = width
        self.h = height
        if self.undo_deq:
            self.undo_deq[0].resize(width, height)

    def on_row_col_seperation(self):
        if self.undo_deq:
            n_plot = TPlot(
                self.undo_deq[0].tiling.row_and_column_separation(), self.w, self.h
            )
            if n_plot is not None:
                self.add(n_plot)

    def on_obstruction_transivity(self):
        if self.undo_deq:
            n_plot = TPlot(
                self.undo_deq[0].tiling.obstruction_transitivity(), self.w, self.h
            )
            if n_plot is not None:
                self.add(n_plot)

    def on_mouse_press(self, x, y, button, modifiers):
        if x > self.w or y > self.h:
            return

        if not self.undo_deq:
            return
        # Find a better way for this...
        # Wrap in a class?

        strats = [
            self.cell_insertion,
            self.cell_insertion_custom,
            self.factor,
            self.factor_with_interleaving,
            lambda x, y, button, modifiers: self.place_point(
                x, y, button, modifiers, DIR_WEST
            ),
            lambda x, y, button, modifiers: self.place_point(
                x, y, button, modifiers, DIR_EAST
            ),
            lambda x, y, button, modifiers: self.place_point(
                x, y, button, modifiers, DIR_NORTH
            ),
            lambda x, y, button, modifiers: self.place_point(
                x, y, button, modifiers, DIR_SOUTH
            ),
            lambda x, y, button, modifiers: self.partial_place_point(
                x, y, button, modifiers, DIR_WEST
            ),
            lambda x, y, button, modifiers: self.partial_place_point(
                x, y, button, modifiers, DIR_EAST
            ),
            lambda x, y, button, modifiers: self.partial_place_point(
                x, y, button, modifiers, DIR_NORTH
            ),
            lambda x, y, button, modifiers: self.partial_place_point(
                x, y, button, modifiers, DIR_SOUTH
            ),
            lambda x, y, button, modifiers: self.fusion(x, y, button, modifiers, True),
            lambda x, y, button, modifiers: self.fusion(x, y, button, modifiers, False),
            lambda x, y, button, modifiers: self.component_fusion(
                x, y, button, modifiers, True
            ),
            lambda x, y, button, modifiers: self.component_fusion(
                x, y, button, modifiers, False
            ),
            self.move,
        ]
        n_plot = strats[self.state.strategy_selected](x, y, button, modifiers)
        if n_plot is not None:
            self.add(TPlot(n_plot, self.w, self.h))

    def move(self, x, y, button, modifiers):

        if button == pyglet.window.mouse.LEFT:
            self.state.move_state.move_type = 0
        elif button == pyglet.window.mouse.RIGHT:
            self.state.move_state.move_type = 1
        else:
            return

        t = self.undo_deq[0]
        self.state.move_state.selected_point = t.get_point_obs_index(Point(x, y))
        if self.state.move_state.selected_point is not None:
            i, j = self.state.move_state.selected_point
            gploc = t.obstruction_locs[i]
            gp = t.tiling.obstructions[i]
        else:
            self.state.move_state.selected_point = t.get_point_req_index(Point(x, y))
            if self.state.move_state.selected_point is not None:
                a, i, j = self.state.move_state.selected_point
                gploc = t.requirement_locs[a][i]
                gp = t.tiling.requirements[a][i]
            else:
                self.state.move_state.reset()
                return

        self.state.move_state.has_selected_pnt = True
        v = gp.patt[j]
        cell = gp.pos[j]
        a, b, c, d = t._cell_to_rect(*cell)
        loc, sz = (a, b), (c, d)
        min_space = 10
        mnx, mny = loc[0] + min_space, loc[1] + min_space
        mxx, mxy = loc[0] + sz[0] - min_space, loc[1] + sz[1] - min_space
        for k in range(len(gp)):
            if k == j - 1:
                mnx = max(mnx, gploc[k].x + min_space)
            if k == j + 1:
                mxx = min(mxx, gploc[k].x - min_space)
            if gp.patt[k] == v - 1:
                mny = max(mny, gploc[k].y + min_space)
            if gp.patt[k] == v + 1:
                mxy = min(mxy, gploc[k].y - min_space)
        self.state.move_state.point_move_bounds = (mnx, mxx, mny, mxy)

        # check click pnt, check btn, set selected in sta
        # print("move")

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):

        if not self.state.move_state.has_selected_pnt or not self.undo_deq:
            return

        t = self.undo_deq[0]
        if len(self.state.move_state.selected_point) == 2:
            i, j = self.state.move_state.selected_point
            mnx, mxx, mny, mxy = self.state.move_state.point_move_bounds
            if self.state.move_state.move_type == 0:
                t.obstruction_locs[i][j] = Point(clamp(x, mnx, mxx), clamp(y, mny, mxy))
            else:
                for k in range(len(t.obstruction_locs[i])):
                    ox, oy = t.obstruction_locs[i][k]
                    ox += dx
                    oy += dy
                    t.obstruction_locs[i][k] = Point(ox, oy)
        else:
            # TODO: does not support types of movement, add that
            # (was not in the original eihter...)
            i, j, k = self.state.move_state.selected_point
            mnx, mxx, mny, mxy = self.state.move_state.point_move_bounds
            t.requirement_locs[i][j][k] = Point(clamp(x, mnx, mxx), clamp(y, mny, mxy),)

    def on_mouse_release(self, x, y, button, modifiers):
        self.state.move_state.reset()

    def cell_insertion(self, x, y, button, modifiers):
        t = self.undo_deq[0]
        cx, cy = t.get_cell(Point(x, y))
        if button == pyglet.window.mouse.LEFT:
            return t.tiling.add_single_cell_requirement(Perm((0,)), (cx, cy))
        elif button == pyglet.window.mouse.RIGHT:
            return t.tiling.add_single_cell_obstruction(Perm((0,)), (cx, cy))

    def cell_insertion_custom(self, x, y, button, modifiers):
        t = self.undo_deq[0]
        cx, cy = t.get_cell(Point(x, y))
        if button == pyglet.window.mouse.LEFT:
            return t.tiling.add_single_cell_requirement(self.custom_placement, (cx, cy))
        elif button == pyglet.window.mouse.RIGHT:
            return t.tiling.add_single_cell_obstruction(self.custom_placement, (cx, cy))

    def place_point(self, x, y, button, modifiers, force_dir=DIR_NONE):
        t = self.undo_deq[0]
        ind = t.get_point_req_index(Point(x, y))
        if ind is not None:
            return t.tiling.place_point_of_gridded_permutation(
                t.tiling.requirements[ind[0]][ind[1]], ind[2], force_dir
            )

    def partial_place_point(self, x, y, button, modifiers, force_dir=DIR_NONE):
        t = self.undo_deq[0]
        ind = t.get_point_req_index(Point(x, y))
        if ind is not None:
            return t.tiling.partial_place_point_of_gridded_permutation(
                t.tiling.requirements[ind[0]][ind[1]], ind[2], force_dir
            )

    def factor(self, x, y, button, modifiers):
        tplot = self.current()
        fac_algo = Factor(tplot.tiling)
        components = fac_algo.get_components()
        facs = fac_algo.factors()
        cell = tplot.get_cell(Point(x, y))
        for fac, component in zip(facs, components):
            if cell in component:
                return fac

    # TODO: combine re-usable part with factor...
    def factor_with_interleaving(self, x, y, button, modifiers):
        tplot = self.current()
        fac_algo = FactorWithInterleaving(tplot.tiling)
        components = fac_algo.get_components()
        facs = fac_algo.factors()
        cell = tplot.get_cell(Point(x, y))
        for fac, component in zip(facs, components):
            if cell in component:
                return fac

    def fusion(self, x, y, button, modifiers, row: bool):
        tplot = self.current()
        c, r = tplot.get_cell(Point(x, y))
        if self.undo_deq:
            try:
                if row:
                    n_plot = TPlot(tplot.tiling.fusion(row=r), self.w, self.h)
                else:
                    n_plot = TPlot(tplot.tiling.fusion(col=c), self.w, self.h)
                if n_plot is not None:
                    self.add(n_plot)
            except (InvalidOperationError, NotImplementedError):
                pass

    def component_fusion(self, x, y, button, modifiers, row: bool):
        tplot = self.current()
        c, r = tplot.get_cell(Point(x, y))
        if self.undo_deq:
            try:
                if row:
                    n_plot = TPlot(tplot.tiling.component_fusion(row=r), self.w, self.h)
                else:
                    n_plot = TPlot(tplot.tiling.component_fusion(col=c), self.w, self.h)
                if n_plot is not None:
                    self.add(n_plot)
            except (InvalidOperationError, NotImplementedError):
                pass

    def on_print_sequence(self):
        if not self.undo_deq:
            return
        print("Generating sequence... ", end=" ")
        t = self.current().tiling
        c = Counter(len(gp) for gp in t.gridded_perms(TPlotManager.MAX_SEQUENCE_SIZE))
        seq = [c[i] for i in range(TPlotManager.MAX_SEQUENCE_SIZE + 1)]
        print(seq)

    def on_print_tiling(self):
        if self.undo_deq:
            tiling = self.current().tiling
            print(f"{str(tiling)}\n\n{repr(tiling)}")

    def on_vertification(self):
        if not self.undo_deq:
            return
        strats = [
            "BasicVerificationStrategy",
            "DatabaseVerificationStrategy",
            "ElementaryVerificationStrategy",
            "InsertionEncodingVerificationStrategy",
            "LocallyFactorableVerificationStrategy",
            "LocalVerificationStrategy",
            "MonotoneTreeVerificationStrategy",
            "OneByOneVerificationStrategy",
        ]
        pad = max(len(s) for s in strats)
        t = self.current().tiling
        verts = [
            BasicVerificationStrategy().verified(t),
            DatabaseVerificationStrategy().verified(t),
            ElementaryVerificationStrategy().verified(t),
            "?",  # InsertionEncodingVerificationStrategy().verified(t),
            LocallyFactorableVerificationStrategy().verified(t),
            LocalVerificationStrategy(no_factors=False).verified(t),
            MonotoneTreeVerificationStrategy().verified(t),
            OneByOneVerificationStrategy().verified(t),
        ]
        print(
            "\n".join(
                f"{strat}{' '*(pad-len(strat))} : {str(vert)}"
                for strat, vert in zip(strats, verts)
            ),
            end="\n\n",
        )


TPlotManager.register_event_type(CustomEvents.ON_EXPORT)
