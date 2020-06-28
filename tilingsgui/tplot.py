"""The tiling drawing tools.
"""

from collections import Counter, deque
from random import uniform
from typing import ClassVar, Deque, List, Optional, Tuple

import pyglet

from permuta import Perm
from permuta.misc import DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST
from tilings import GriddedPerm, Tiling
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
    """A single tiling image.
    """

    _OBSTRUCTION_COLOR: ClassVar[Tuple[float, float, float]] = Color.RED
    _REQUIREMENT_COLOR: ClassVar[Tuple[float, float, float]] = Color.BLUE
    _HIGHLIGHT_COLOR: ClassVar[Tuple[float, float, float]] = Color.ORANGE
    _EMPTY_COLOR: ClassVar[Tuple[float, float, float]] = Color.GRAY
    _SHADED_CELL_COLOR: ClassVar[Tuple[float, float, float]] = Color.GRAY
    _FUZZYNESS = 0.25  # Should be in [0,0.5)
    _CLICK_PRECISION_SQUARED: int = 100
    _POINT_SIZE = 5
    _PRETTY_POINT_SIZE = 10

    @staticmethod
    def _col_row_and_count(
        g_perm: GriddedPerm, grid_size: Tuple[int, int]
    ) -> Tuple[List[int], List[int], List[List[int]], List[List[int]]]:
        """Computes data used to positions gridded permutations correctly.

        Args:
            g_perm (GriddedPerm): The gridded permutations that needs to be positioned.
            grid_size (Tuple[int, int]): The tiling's dimension.

        Returns:
            Tuple[List[int], List[int], List[List[int]], List[List[int]]]: The first
            element counts how many points land in each column, the second does the
            same but for rows. The last two contain info about which column has which
            index of element and which row has which element.
        """
        colcount = [0] * grid_size[0]
        rowcount = [0] * grid_size[1]
        col: List[List[int]] = [[] for i in range(grid_size[0])]
        row: List[List[int]] = [[] for i in range(grid_size[1])]
        for ind, ((c_x, c_y), val) in enumerate(zip(g_perm.pos, g_perm.patt)):
            colcount[c_x] += 1
            rowcount[c_y] += 1
            col[c_x].append(ind)
            row[c_y].append(val)
        for r in row:
            r.sort()
        return colcount, rowcount, col, row

    @staticmethod
    def gridded_perm_initial_locations(
        g_perm: GriddedPerm, grid_size: Tuple[int, int], cell_size: Tuple[float, float]
    ) -> List[Point]:
        """Calculate coordinates for all points in a gridded permutations.

        Args:
            g_perm (GriddedPerm): The gridded permutation to convert to positions.
            grid_size (Tuple[int, int]): The tiling's dimension.
            cell_size (Tuple[float, float]): The size (w,h) of each cell.

        Returns:
            List[Point]: A list of positions.
        """
        colcount, rowcount, col, row = TPlot._col_row_and_count(g_perm, grid_size)
        return [
            Point(
                cell_size[0]
                * (
                    c_x
                    + (
                        col[c_x].index(ind)
                        + 1
                        + uniform(-TPlot._FUZZYNESS, TPlot._FUZZYNESS)
                    )
                    / (colcount[c_x] + 1)
                ),
                cell_size[1]
                * (
                    c_y
                    + (
                        row[c_y].index(val)
                        + 1
                        + uniform(-TPlot._FUZZYNESS, TPlot._FUZZYNESS)
                    )
                    / (rowcount[c_y] + 1)
                ),
            )
            for ind, ((c_x, c_y), val) in enumerate(zip(g_perm.pos, g_perm.patt))
        ]

    def __init__(self, tiling: Tiling, w: float, h: float) -> None:
        """Create an instance of a tiling plot.

        Args:
            tiling (Tiling): The tiling to draw.
            w (float): The width of the drawing.
            h (float): The height of the drawing.
        """
        t_w, t_h = tiling.dimensions

        self.tiling: Tiling = tiling
        self._w: float = w
        self._h: float = h
        self._obstruction_locs: List[List[Point]] = [
            TPlot.gridded_perm_initial_locations(gp, (t_w, t_h), (w / t_w, h / t_h))
            for gp in self.tiling.obstructions
        ]
        self._requirement_locs: List[List[List[Point]]] = [
            [
                TPlot.gridded_perm_initial_locations(gp, (t_w, t_h), (w / t_w, h / t_h))
                for gp in reqlist
            ]
            for reqlist in self.tiling.requirements
        ]

    def draw(self, state: GuiState, mpos: Point) -> None:
        """Draw the tiling.

        Args:
            state (GuiState): A collection of settings.
            mpos (Point): The current mouse position.
        """
        if any(len(obs) == 0 for obs in self.tiling.obstructions):
            GeoDrawer.draw_rectangle(0, 0, self._w, self._h, TPlot._EMPTY_COLOR)
        else:
            if state.shading:
                self._draw_shaded_cells()
            self._draw_grid()
            self._draw_obstructions(state, mpos)
            self._draw_requirements(state, mpos)

    def resize(self, width: int, height: int) -> None:
        """Resize the image.

        Args:
            width (int): The new width.
            height (int): The new height.
        """
        for obs in self._obstruction_locs:
            for pnt in obs:
                pnt.x = pnt.x / self._w * width
                pnt.y = pnt.y / self._h * height
        for reqlist in self._requirement_locs:
            for req in reqlist:
                for pnt in req:
                    pnt.x = pnt.x / self._w * width
                    pnt.y = pnt.y / self._h * height
        self._w = width
        self._h = height

    def get_cell(self, mpos: Point) -> Tuple[int, int]:
        """Get the 2d index of the cell that was clicked.

        Args:
            mpos (Point): The current mouse position.

        Returns:
            Tuple[int, int]: The 2d index (column, row).
        """
        t_w, t_h = self.tiling.dimensions
        c_w, c_h = self._w / t_w, self._h / t_h
        c_x, c_y = int(mpos.x / c_w), int(mpos.y / c_h)
        return c_x, c_y

    def get_point_obs_index(self, mpos: Point) -> Optional[Tuple[int, int]]:
        """Look for an obstruction point that collides with the mouse click.
        If one is found, the index of its gridded permutation and its index
        within the gridded permutation is returned. If not, None is returned.

        Args:
            mpos (Point): The current mouse position.

        Returns:
            Optional[Tuple[int, int]]: A tuple of the index of gridded permutation
            containing point and the index of point within gridded permutation, if
            one is found, None otherwise.
        """
        for j, loc in enumerate(self._obstruction_locs):
            for k, pnt in enumerate(loc):
                if mpos.dist_squared_to(pnt) <= TPlot._CLICK_PRECISION_SQUARED:
                    return j, k
        return None

    def get_point_req_index(self, mpos: Point) -> Optional[Tuple[int, int, int]]:
        """Look for an requirement point that collides with the mouse click.
        If one is found, the index of its requirement list, gridded permutation
        within the requirement list and its index within the gridded permutation
        is returned. If not, None is returned.

        Args:
            mpos (Point): The current mouse position.

        Returns:
            Optional[Tuple[int, int, int]]: A tuple of the index of the requirement
            list, the index of the gridded permutation within the requirement list
            and the index of point within gridded permutation, that collides with
            the click, if one is found, None otherwise.
        """
        for i, reqlist in enumerate(self._requirement_locs):
            for j, loc in enumerate(reqlist):
                for k, pnt in enumerate(loc):
                    if mpos.dist_squared_to(pnt) <= TPlot._CLICK_PRECISION_SQUARED:
                        return i, j, k
        return None

    def _cell_to_rect(self, c_x: int, c_y: int) -> Tuple[float, float, float, float]:
        """Get the rectangle for a cell.

        Args:
            c_x (int): The column of the cell.
            c_y (int): The row of the cell.

        Returns:
            Tuple[float, float, float, float]: A tuple with (x, y, w, h) where (x, y)
            is the coordinate of the rectangles bottom left corner and w and h are
            his width and height respectively.
        """
        t_w, t_h = self.tiling.dimensions
        c_w, c_h = self._w / t_w, self._h / t_h
        return c_x * c_w, c_y * c_h, c_w, c_h

    def _draw_shaded_cells(self) -> None:
        """Draw all cells with a single point obstruction as a filled rectangle.
        """
        for c_x, c_y in self.tiling.empty_cells:
            GeoDrawer.draw_rectangle(
                *self._cell_to_rect(c_x, c_y), TPlot._SHADED_CELL_COLOR
            )

    def _draw_obstructions(self, state: GuiState, mpos: Point) -> None:
        """Draw all obstructions.

        Args:
            state (GuiState): A collection of settings.
            mpos (Point): The current mouse position.
        """
        point_cells_with_point_perm_req = self.tiling.point_cells.intersection(
            {
                req.pos[0]
                for req_lis in self.tiling.requirements
                for req in req_lis
                if req.is_point_perm()
            }
        )
        hover_cell = self.get_cell(mpos)
        for obs, loc in zip(self.tiling.obstructions, self._obstruction_locs):
            if (state.shading and obs.is_point_perm()) or (
                state.pretty_points
                and all(p in point_cells_with_point_perm_req for p in obs.pos)
            ):
                continue
            col = (
                TPlot._HIGHLIGHT_COLOR
                if state.highlight_touching_cell
                and any(p == hover_cell for p in obs.pos)
                else TPlot._OBSTRUCTION_COLOR
            )
            localized = obs.is_localized()
            if (localized and state.show_localized) or (
                not localized and state.show_crossing
            ):
                GeoDrawer.draw_point_path(loc, col, TPlot._POINT_SIZE)

    def _draw_requirements(self, state: GuiState, mpos: Point) -> None:
        """Draw all requirements.

        Args:
            state (GuiState): A collection of settings.
            mpos (Point): The current mouse position.
        """
        hover_index = self.get_point_req_index(mpos)
        for i, reqlist in enumerate(self._requirement_locs):
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
                GeoDrawer.draw_circle(
                    pnt.x, pnt.y, TPlot._PRETTY_POINT_SIZE, Color.BLACK
                )
                continue
            col = (
                TPlot._HIGHLIGHT_COLOR
                if hover_index is not None and i == hover_index[0]
                else TPlot._REQUIREMENT_COLOR
            )
            for j, loc in enumerate(reqlist):
                localized = self.tiling.requirements[i][j].is_localized()
                if (localized and state.show_localized) or (
                    not localized and state.show_crossing
                ):
                    GeoDrawer.draw_point_path(loc, col, 5)

    def _draw_grid(self) -> None:
        """Draw the tiling's grid.
        """
        t_w, t_h = self.tiling.dimensions
        for i in range(t_w):
            x = self._w * i / t_w
            GeoDrawer.draw_line_segment(x, self._h, x, 0, Color.BLACK)
        for i in range(t_h):
            y = self._h * i / t_h
            GeoDrawer.draw_line_segment(0, y, self._w, y, Color.BLACK)


# TODO: CLEAN!
class TPlotManager(pyglet.event.EventDispatcher, Observer):
    MAX_DEQUEUE_SIZE: ClassVar[int] = 100
    MAX_SEQUENCE_SIZE = 7

    def __init__(self, width: int, height: int, state: GuiState, dispatchers=()):
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
            gploc = t._obstruction_locs[i]
            gp = t.tiling.obstructions[i]
        else:
            self.state.move_state.selected_point = t.get_point_req_index(Point(x, y))
            if self.state.move_state.selected_point is not None:
                a, i, j = self.state.move_state.selected_point
                gploc = t._requirement_locs[a][i]
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
                t._obstruction_locs[i][j] = Point(
                    clamp(x, mnx, mxx), clamp(y, mny, mxy)
                )
            else:
                for k in range(len(t._obstruction_locs[i])):
                    ox, oy = t._obstruction_locs[i][k]
                    ox += dx
                    oy += dy
                    t._obstruction_locs[i][k] = Point(ox, oy)
        else:
            # TODO: does not support types of movement, add that
            # (was not in the original eihter...)
            i, j, k = self.state.move_state.selected_point
            mnx, mxx, mny, mxy = self.state.move_state.point_move_bounds
            t._requirement_locs[i][j][k] = Point(
                clamp(x, mnx, mxx), clamp(y, mny, mxy),
            )

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
