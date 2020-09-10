"""The tiling drawing tools.
"""

import json
from collections import Counter, deque
from random import uniform
from typing import Callable, ClassVar, Deque, Iterable, List, Tuple

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
    InsertionEncodingVerificationStrategy,
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
    """A single tiling image."""

    REQ_NOT_FOUND: ClassVar[Tuple[int, int, int]] = (-1, -1, -1)
    OBS_NOT_FOUND: ClassVar[Tuple[int, int]] = (-1, -1)
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

    def get_requirement_gridded_perm_locations(
        self, requirement_list_index: int, gridded_perm_index: int
    ) -> List[Point]:
        """Get a gridded perm as locations of points from requirements.

        Args:
            requirement_list_index (int): The requirement list it belongs to.
            gridded_perm_index (int): The index of the gridded perm within
            the requirement list.

        Returns:
            List[Point]: A gridded perm as a list of points.
        """
        return self._requirement_locs[requirement_list_index][gridded_perm_index]

    def get_obstruction_gridded_perm_location(
        self, gridded_perm_index: int
    ) -> List[Point]:
        """Get a gridded perm as locations of points from obstructions.

        Args:
            gridded_perm_index (int): The index of the gridded perm.

        Returns:
            List[Point]: A gridded perm as a list of points.
        """
        return self._obstruction_locs[gridded_perm_index]

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

    def get_point_obs_index(self, mpos: Point) -> Tuple[int, int]:
        """Look for an obstruction point that collides with the mouse click.
        If one is found, the index of its gridded permutation and its index
        within the gridded permutation is returned. If not, (-1,-1) is returned.

        Args:
            mpos (Point): The current mouse position.

        Returns:
            Tuple[int, int]: A tuple of the index of gridded permutation
            containing point and the index of point within gridded permutation, if
            one is found, (-1,-1) pair otherwise.
        """
        for j, loc in enumerate(self._obstruction_locs):
            for k, pnt in enumerate(loc):
                if mpos.dist_squared_to(pnt) <= TPlot._CLICK_PRECISION_SQUARED:
                    return j, k
        return TPlot.OBS_NOT_FOUND

    def get_point_req_index(self, mpos: Point) -> Tuple[int, int, int]:
        """Look for an requirement point that collides with the mouse click.
        If one is found, the index of its requirement list, gridded permutation
        within the requirement list and its index within the gridded permutation
        is returned. If not, (-1,-1,-1) is returned.

        Args:
            mpos (Point): The current mouse position.

        Returns:
            Tuple[int, int, int]: A tuple of the index of the requirement
            list, the index of the gridded permutation within the requirement list
            and the index of point within gridded permutation, that collides with
            the click, if one is found, (-1,-1,-1) otherwise.
        """
        for i, reqlist in enumerate(self._requirement_locs):
            for j, loc in enumerate(reqlist):
                for k, pnt in enumerate(loc):
                    if mpos.dist_squared_to(pnt) <= TPlot._CLICK_PRECISION_SQUARED:
                        return i, j, k
        return TPlot.REQ_NOT_FOUND

    def cell_to_rect(self, c_x: int, c_y: int) -> Tuple[float, float, float, float]:
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
        """Draw all cells with a single point obstruction as a filled rectangle."""
        for c_x, c_y in self.tiling.empty_cells:
            GeoDrawer.draw_rectangle(
                *self.cell_to_rect(c_x, c_y), TPlot._SHADED_CELL_COLOR
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
        hover_index, _ = self.get_point_obs_index(mpos)
        hover_cell = self.get_cell(mpos)
        for i, (obs, loc) in enumerate(
            zip(self.tiling.obstructions, self._obstruction_locs)
        ):
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
            if hover_index == i:
                col = TPlot._HIGHLIGHT_COLOR
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
                if hover_index != TPlot.REQ_NOT_FOUND and i == hover_index[0]
                else TPlot._REQUIREMENT_COLOR
            )
            for j, loc in enumerate(reqlist):
                localized = self.tiling.requirements[i][j].is_localized()
                if (localized and state.show_localized) or (
                    not localized and state.show_crossing
                ):
                    GeoDrawer.draw_point_path(loc, col, 5)

    def _draw_grid(self) -> None:
        """Draw the tiling's grid."""
        t_w, t_h = self.tiling.dimensions
        for i in range(t_w):
            x = self._w * i / t_w
            GeoDrawer.draw_line_segment(x, self._h, x, 0, Color.BLACK)
        for i in range(t_h):
            y = self._h * i / t_h
            GeoDrawer.draw_line_segment(0, y, self._w, y, Color.BLACK)

    def to_tikz(self) -> None:
        """Output tikz drawing."""
        print("\\begin{tikzpicture}[scale=1, every node/.style={scale=1}]")
        print("\t\\def\\xscale{1.0} % Horizontal scale factor")
        print("\t\\def\\yscale{1.0} % Vertical scale factor")
        print("\t\\def\\spnt{0.075} % Size of smaller points")
        print("\t\\def\\lpnt{0.125} % Size of larger points")
        self._tikz_shaded()
        self._tikz_grid()
        self._tikz_obstructions()
        self._tikz_requirements()
        print("\\end{tikzpicture}", flush=True)

    def _tikz_shaded(self):
        for c_x, c_y in self.tiling.empty_cells:
            x, y, w, h = self.cell_to_rect(c_x, c_y)
            x1, y1, x2, y2 = x / 100, y / 100, (x + w) / 100, (y + h) / 100
            print(
                f"\t\\fill[gray!80] ({x1}*\\xscale,{y1}*\\yscale)"
                f" rectangle ({x2}*\\xscale,{y2}*\\yscale);"
            )

    def _tikz_grid(self) -> None:
        t_w, t_h = self.tiling.dimensions
        for i in range(t_w + 1):
            x = self._w * i / t_w
            print(
                f"\t\\draw ({x / 100}*\\xscale, {self._h / 100}*\\yscale) -- "
                f"({x / 100}*\\xscale, 0);"
            )
        for i in range(t_h + 1):
            y = self._h * i / t_h
            print(
                f"\t\\draw (0, {y / 100}*\\yscale) -- "
                f"({self._w / 100}*\\xscale, {y / 100}*\\yscale);"
            )

    def _tikz_obstructions(self) -> None:

        point_cells_with_point_perm_req = self.tiling.point_cells.intersection(
            {
                req.pos[0]
                for req_lis in self.tiling.requirements
                for req in req_lis
                if req.is_point_perm()
            }
        )
        for obs, loc in zip(self.tiling.obstructions, self._obstruction_locs):
            if obs.is_point_perm() or all(
                p in point_cells_with_point_perm_req for p in obs.pos
            ):
                continue
            TPlot._tikz_pnt_path(loc, "red")

    def _tikz_requirements(self) -> None:
        for i, reqlist in enumerate(self._requirement_locs):
            if len(reqlist[0]) == 1 and any(
                p in self.tiling.point_cells
                for req in self.tiling.requirements[i]
                for p in req.pos
            ):
                pnt = reqlist[0][0]
                print(
                    f"\t\\fill ({pnt.x/100}*\\xscale,"
                    f"{pnt.y/100}*\\yscale) circle (\\lpnt);"
                )
                continue
            for loc in reqlist:
                TPlot._tikz_pnt_path(loc, "blue")

    @staticmethod
    def _tikz_pnt_path(loc: List[Point], col: str) -> None:
        if not loc:
            return
        print(
            f"\t\\fill[{col}] ({loc[0].x/100}*\\xscale, "
            f"{loc[0].y/100}*\\yscale) circle (\\spnt);"
        )
        if len(loc) == 1:
            return
        path = f"({loc[0].x/100}*\\xscale, {loc[0].y/100}*\\yscale)"
        for pnt in loc[1:]:
            x, y = pnt.x, pnt.y
            path += f" -- ({x/100}*\\xscale,{y/100}*\\yscale)"
            print(
                f"\t\\fill[{col}] ({x/100}*\\xscale, {y/100}*\\yscale) circle (\\spnt);"
            )
        print(f"\t\\draw[{col}] {path};")


Action = Callable[[int, int, int, int], None]


class TPlotManager(pyglet.event.EventDispatcher, Observer):
    """A manager that handles drawing the tiling plot and observing
    events that have to do with it. It halso handles dispatching some
    events and memory for undo and redos.
    """

    _MAX_DEQUEUE_SIZE: ClassVar[int] = 100
    _MAX_SEQUENCE_SIZE: ClassVar[int] = 7
    _VERIFICATION_STRATS: ClassVar[List[str]] = [
        "BasicVerificationStrategy",
        "DatabaseVerificationStrategy",
        "ElementaryVerificationStrategy",
        "InsertionEncodingVerificationStrategy",
        "LocallyFactorableVerificationStrategy",
        "LocalVerificationStrategy",
        "MonotoneTreeVerificationStrategy",
        "OneByOneVerificationStrategy",
    ]
    _POINT_PERM: ClassVar[Perm] = Perm((0,))
    _MIN_SPACE: ClassVar[int] = 10

    @staticmethod
    def _verify(tiling: Tiling) -> List[str]:
        """Apply all verification strategies on a tiling.

        Args:
            tiling (Tiling): The tiling to apply strategies to.

        Returns:
            List[str]: A list of boolean results, converted to strings.
        """
        return [
            str(BasicVerificationStrategy().verified(tiling)),
            str(DatabaseVerificationStrategy().verified(tiling)),
            str(ElementaryVerificationStrategy().verified(tiling)),
            str(InsertionEncodingVerificationStrategy().verified(tiling)),
            str(LocallyFactorableVerificationStrategy().verified(tiling)),
            str(LocalVerificationStrategy(no_factors=False).verified(tiling)),
            str(MonotoneTreeVerificationStrategy().verified(tiling)),
            str(OneByOneVerificationStrategy().verified(tiling)),
        ]

    def __init__(
        self,
        width: int,
        height: int,
        state: GuiState,
        dispatchers: Iterable[pyglet.event.EventDispatcher] = (),
    ) -> None:
        """Create an instance of a tiling plot manager.

        Args:
            width (int): The width to use for the drawing
            height (int): The height to use for the drawing.
            state (GuiState): The current state for various settings.
            dispatchers (Iterable[pyglet.event.EventDispatcher], optional): A collection
            of dispatchers that this observer should listen ot. Defaults to ().
        """
        Observer.__init__(self, dispatchers)
        self.deques: List[Deque[TPlot]] = [deque(), deque()]
        self._mouse_pos: Point = Point(0, 0)
        self._custom_data: str = "01"
        self._state: GuiState = state
        self._w: int = width
        self._h: int = height
        self._actions: List[Action] = self._get_actions()
        self.position(width, height)

    def position(self, width: int, height: int) -> None:
        """Resize the tiling plot canvas.

        Args:
            width (int): The new width.
            height (int): The new height.
        """
        self._w = width
        self._h = height
        if not self._empty():
            self._current().resize(width, height)

    ##################
    # Event Handlers #
    ##################

    def on_draw(self) -> bool:
        """Draw event handler. Draws the current tiling plot if any.

        Returns:
            bool: False as we do not want to consume event.
        """
        if not self._empty():
            self._current().draw(self._state, self._mouse_pos)
        return False

    def on_fetch_tiling_for_export(self) -> bool:
        """Event for request for exporting the current tiling. We dispatch our
        own event here for the export observer to deal with it.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            self.dispatch_event(
                CustomEvents.ON_EXPORT, self._current().tiling.to_jsonable()
            )
        return True

    def on_basis_input(self, basis: str) -> bool:
        """Event handler for processing basis input.

        Args:
            basis (str): The input.

        Returns:
            bool: True as we want to consume the event.
        """
        self._add_plot(TPlot(Tiling.from_string(basis), self._w, self._h))
        return True

    def on_tiling_json_input(self, basis: Tiling) -> bool:
        """Event handler for processing tiling input.

        Args:
            basis (Tiling): A tiling object.

        Returns:
            bool: True as we want to consume the event.
        """
        self._add_plot(TPlot(basis, self._w, self._h))
        return True

    def on_placement_input(self, txt: str) -> bool:
        """Event handler for setting the custom placement permutation.

        Args:
            txt (str): The upper right input field data.

        Returns:
            bool: True as we want to consume the event.
        """
        self._custom_data = txt
        return True

    def on_row_col_seperation(self) -> bool:
        """Event handler for applying row column seperation on the current tiling
        if any.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            n_plot = TPlot(
                self._current().tiling.row_and_column_separation(), self._w, self._h
            )
            if n_plot is not None:
                self._add_plot(n_plot)
        return True

    def on_obstruction_transivity(self) -> bool:
        """Event handler for applying obstruction transivity on the current tiling
        if any.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            n_plot = TPlot(
                self._current().tiling.obstruction_transitivity(), self._w, self._h
            )
            if n_plot is not None:
                self._add_plot(n_plot)
        return True

    def on_print_sequence(self) -> bool:
        """Event handler for printing the sequence of number of griddable permutations
        on the current tiling. It does so up to a max length.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            print("Sequence: ", end="")
            c = Counter(
                len(gp)
                for gp in self._current().tiling.gridded_perms(
                    TPlotManager._MAX_SEQUENCE_SIZE
                )
            )
            print(
                ", ".join(str(c[i]) for i in range(TPlotManager._MAX_SEQUENCE_SIZE + 1))
            )
        return True

    def on_print_tiling(self) -> bool:
        """Event handler for printing the current tiling if any. Prints both the str
        and repr format of the tiling.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            tiling = self._current().tiling
            json_str = json.dumps(tiling.to_jsonable())
            print(f"{str(tiling)}\n\n{repr(tiling)}\n\n{json_str}\n")
        return True

    def on_tikz(self) -> bool:
        """Event handler for printing current tiling as tikz.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            self._current().to_tikz()
        return True

    def on_obstruction_inferral(self) -> bool:
        """Event handler for obstruction inferral.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            length = 3
            if self._custom_data and self._custom_data.isnumeric():
                length = max(min(6, int(self._custom_data)), 0)
            tiling = self._current().tiling
            self._add_tiling(tiling.all_obstruction_inferral(length))
        return True

    def on_verification(self) -> bool:
        """Event handler for verification on the current tiling.

        Returns:
            bool: True as we want to consume the event.
        """
        if not self._empty():
            pad = max(len(s) for s in TPlotManager._VERIFICATION_STRATS)
            print(
                "\n".join(
                    f"{strat}{' '*(pad-len(strat))} : {vert}"
                    for strat, vert in zip(
                        TPlotManager._VERIFICATION_STRATS,
                        TPlotManager._verify(self._current().tiling),
                    )
                ),
                end="\n\n",
            )
        return True

    def on_undo(self) -> bool:
        """Event handler for undo.

        Returns:
            bool: True as we want to consume event.
        """
        if len(self._undo_deq()) > 1:
            self._redo_deq().append(self._undo_deq().popleft())
            self._current().resize(self._w, self._h)
        return True

    def on_redo(self) -> bool:
        """Event handler for redo.

        Returns:
            bool: True as we want to consume event.
        """
        if self._redo_deq():
            self._undo_deq().appendleft(self._redo_deq().pop())
            self._current().resize(self._w, self._h)
        return True

    def on_mouse_motion(self, x: int, y: int, _dx: int, _dy: int) -> bool:
        """Event hander for when the mouse is moved.

        Args:
            x (int): The x coordinate of the mouse.
            y (int): The y coordinate of the mouse.
            _dx (int): The horizontal distance moved since last time the event
            was dispatched. This is unused.
            _dy (int): The vertical distance moved since last time the event
            was dispatched. This is unused.

        Returns:
            bool: False as the event is not consumed here.
        """
        self._mouse_pos.x = x
        self._mouse_pos.y = y
        return False

    def on_mouse_release(self, _x: int, _y: int, _button: int, _modifiers: int) -> bool:
        """Event handler for when the mouse button is released.

        Args:
            _x (int): The x coordinate of the mouse. Unused.
            _y (int): The y coordinate of the mouse. Unused.
            _button (int): Which button was released. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.

        Returns:
            bool: False as we do not want to consume this event.
        """
        self._state.move_state.reset()
        return False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool:
        """On mouse click event handler.

        Args:
            x (int): The x coordinate of the click.
            y (int): The y coordinate of the click.
            button (int): The mouse button that was clicked.
            modifiers (int): If combinded with modifiers (e.g. ctrl).

        Returns:
            bool: False as we do not want to consume this event.
        """
        if x < self._w and y < self._h and not self._empty():
            self._actions[self._state.action_selected](x, y, button, modifiers)
        return False

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, _button: int, _modifiers: int
    ) -> bool:
        """Event handler for draggin the mouse.

        Args:
            x (int): The x coordinate of the click.
            y (int): The y coordinate of the click.
            dx (int): The horizontal distance moved.
            dy (int): The vertical distance moved.
            _button (int): The mouse button that was clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.

        Returns:
            bool: False as we do not want to consume this event.
        """

        if not self._state.move_state.has_selected_pnt or self._empty():
            return False

        tplot = self._current()

        if len(self._state.move_state.selected_point) == 2:
            # If moving obstruction
            i, j = self._state.move_state.selected_point
            mnx, mxx, mny, mxy = self._state.move_state.point_move_bounds
            if self._state.move_state.move_type == 0:
                # Moving a single point, must confine to the permutation's structure.
                pnt = tplot.get_obstruction_gridded_perm_location(i)[j]
                pnt.x, pnt.y = clamp(x, mnx, mxx), clamp(y, mny, mxy)
            else:
                # Moving all, , must confine to the permutation's structure.
                all_pos = tplot.tiling.obstructions[i].pos
                for k in range(len(tplot.get_obstruction_gridded_perm_location(i))):
                    pnt = tplot.get_obstruction_gridded_perm_location(i)[k]
                    if (
                        pnt.x + dx < 0
                        or pnt.y + dy < 0
                        or all_pos[k] != tplot.get_cell(Point(pnt.x + dx, pnt.y + dy))
                    ):
                        return False

                for k in range(len(tplot.get_obstruction_gridded_perm_location(i))):
                    pnt = tplot.get_obstruction_gridded_perm_location(i)[k]
                    pnt.x += dx
                    pnt.y += dy
        else:
            # If moving requirement
            i, j, k = self._state.move_state.selected_point
            mnx, mxx, mny, mxy = self._state.move_state.point_move_bounds
            pnt = tplot.get_requirement_gridded_perm_locations(i, j)[k]
            pnt.x, pnt.y = clamp(x, mnx, mxx), clamp(y, mny, mxy)
        return False

    ###################
    # Private helpers #
    ###################

    def _undo_deq(self) -> Deque[TPlot]:
        """Getter for the undo deque.

        Returns:
            Deque[TPlot]: The undo deque.
        """
        return self.deques[0]

    def _redo_deq(self) -> Deque[TPlot]:
        """Getter for the redo deque.

        Returns:
            Deque[TPlot]: The redo deque.
        """
        return self.deques[1]

    def _empty(self) -> bool:
        """Is there currently a tiling plot?

        Returns:
            bool: True iff no tiling plot.
        """
        return not self

    def _current(self) -> TPlot:
        """Get the current tiling plot.

        Returns:
            TPlot: The tiling plot currently being rendered.
        """
        return self._undo_deq()[0]

    def _add_plot(self, drawing: TPlot) -> None:
        """Add a new tiling plot, overtaking the current one if any.

        Args:
            drawing (TPlot): The new tiling plot to render.
        """
        self._undo_deq().appendleft(drawing)
        self._redo_deq().clear()
        if len(self._undo_deq()) > TPlotManager._MAX_DEQUEUE_SIZE:
            self._undo_deq().pop()

    def _add_tiling(self, tiling: Tiling) -> None:
        """Add a new tiling plot, overtaking the current one if any.

        Args:
            tiling (Tiling): The tiling to use to create a tiling plot.
        """
        self._add_plot(TPlot(tiling, self._w, self._h))

    def _factor_from_algorithm(self, cell: Tuple[int, int], fac_algo: Factor) -> None:
        """Helper for factor actions.

        Args:
            cell (Tuple[int, int]): The clicked cell.
            fac_algo (Factor): The facorize algorithm to use.
        """
        components = fac_algo.get_components()
        facs = fac_algo.factors()
        for fac, component in zip(facs, components):
            if cell in component:
                self._add_tiling(fac)
                break

    def _set_move_boundaries(
        self,
        indices: Tuple[int, ...],
        gp_loc: List[Point],
        g_perm: GriddedPerm,
        tplot: TPlot,
    ) -> None:
        """Set the move boundaries so that the permutation pattern is not broken.

        Args:
            indices (Tuple[int, ...]): The indices for the permutation within either
            obstructions or requirements.
            gp_loc (List[Point]): The location of the gridded permutation's points.
            g_perm (GriddedPerm): The gridded permutation that is being moved.
            tplot (TPlot): The current tiling plot.
        """
        perm_elem = g_perm.patt[indices[-1]]
        rect_x, rect_y, rect_w, rect_h = tplot.cell_to_rect(*g_perm.pos[indices[-1]])
        mnx, mny = rect_x + TPlotManager._MIN_SPACE, rect_y + TPlotManager._MIN_SPACE
        mxx, mxy = (
            rect_x + rect_w - TPlotManager._MIN_SPACE,
            rect_y + rect_h - TPlotManager._MIN_SPACE,
        )
        for k in range(len(g_perm)):
            if k == indices[-1] - 1:
                mnx = max(mnx, gp_loc[k].x + TPlotManager._MIN_SPACE)
            if k == indices[-1] + 1:
                mxx = min(mxx, gp_loc[k].x - TPlotManager._MIN_SPACE)
            if g_perm.patt[k] == perm_elem - 1:
                mny = max(mny, gp_loc[k].y + TPlotManager._MIN_SPACE)
            if g_perm.patt[k] == perm_elem + 1:
                mxy = min(mxy, gp_loc[k].y - TPlotManager._MIN_SPACE)
        self._state.move_state.point_move_bounds = (mnx, mxx, mny, mxy)

    def _get_actions(self) -> List[Action]:
        """Construct the list of actions.

        Returns:
            List[Action]: List of actions.
        """
        return [
            self._cell_insertion,
            self._cell_insertion_custom,
            self._factor,
            self._factor_with_interleaving,
            lambda x, y, button, modifiers: self._place_point(
                x, y, button, modifiers, DIR_WEST
            ),
            lambda x, y, button, modifiers: self._place_point(
                x, y, button, modifiers, DIR_EAST
            ),
            lambda x, y, button, modifiers: self._place_point(
                x, y, button, modifiers, DIR_NORTH
            ),
            lambda x, y, button, modifiers: self._place_point(
                x, y, button, modifiers, DIR_SOUTH
            ),
            lambda x, y, button, modifiers: self._partial_place_point(
                x, y, button, modifiers, DIR_WEST
            ),
            lambda x, y, button, modifiers: self._partial_place_point(
                x, y, button, modifiers, DIR_EAST
            ),
            lambda x, y, button, modifiers: self._partial_place_point(
                x, y, button, modifiers, DIR_NORTH
            ),
            lambda x, y, button, modifiers: self._partial_place_point(
                x, y, button, modifiers, DIR_SOUTH
            ),
            lambda x, y, button, modifiers: self._fusion(x, y, button, modifiers, True),
            lambda x, y, button, modifiers: self._fusion(
                x, y, button, modifiers, False
            ),
            lambda x, y, button, modifiers: self._component_fusion(
                x, y, button, modifiers, True
            ),
            lambda x, y, button, modifiers: self._component_fusion(
                x, y, button, modifiers, False
            ),
            self._move,
        ]

    def __bool__(self) -> bool:
        """The bool conversion of self tells if there is currently a tiling plot.

        Returns:
            bool: True iff there is a tiling plot.
        """
        return bool(self._undo_deq())

    ###########
    # Actions #
    ###########

    def _move(self, x: int, y: int, button: int, _modifiers: int) -> None:
        """The moving action. Tries to find a clicked point and if so, set state
        to it as a moving point and calculates boundaries it can move within.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            button (int): The mouse button clicked.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
        """
        if button == pyglet.window.mouse.LEFT:
            self._state.move_state.move_type = 0
        elif button == pyglet.window.mouse.RIGHT:
            self._state.move_state.move_type = 1
        else:
            return

        tplot = self._current()
        idxs: Tuple[int, ...] = tplot.get_point_obs_index(Point(x, y))
        if idxs != TPlot.OBS_NOT_FOUND:
            self._state.move_state.selected_point = idxs
            gp_loc = tplot.get_obstruction_gridded_perm_location(idxs[0])
            g_perm = tplot.tiling.obstructions[idxs[0]]
        else:
            idxs = tplot.get_point_req_index(Point(x, y))
            if idxs != TPlot.REQ_NOT_FOUND:
                self._state.move_state.selected_point = idxs
                gp_loc = tplot.get_requirement_gridded_perm_locations(idxs[0], idxs[1])
                g_perm = tplot.tiling.requirements[idxs[0]][idxs[1]]
            else:
                self._state.move_state.reset()
                return

        self._state.move_state.has_selected_pnt = True
        self._set_move_boundaries(idxs, gp_loc, g_perm, tplot)

    def _cell_insertion(self, x: int, y: int, button: int, _modifiers: int) -> None:
        """Add a length 1 obstruction or requirement to a single cell.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            button (int): The mouse button clicked.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
        """
        tplot = self._current()
        if button == pyglet.window.mouse.LEFT:
            self._add_tiling(
                tplot.tiling.add_single_cell_requirement(
                    TPlotManager._POINT_PERM, tplot.get_cell(Point(x, y))
                )
            )
        elif button == pyglet.window.mouse.RIGHT:
            self._add_tiling(
                tplot.tiling.add_single_cell_obstruction(
                    TPlotManager._POINT_PERM, tplot.get_cell(Point(x, y))
                )
            )

    def _cell_insertion_custom(
        self, x: int, y: int, button: int, _modifiers: int
    ) -> None:
        """Add a custom obstruction or requirement to a single cell.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            button (int): The mouse button clicked.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
        """
        tplot = self._current()
        if button == pyglet.window.mouse.LEFT:
            self._add_tiling(
                tplot.tiling.add_single_cell_requirement(
                    Perm.standardize(self._custom_data),
                    tplot.get_cell(Point(x, y)),
                )
            )
        elif button == pyglet.window.mouse.RIGHT:
            self._add_tiling(
                tplot.tiling.add_single_cell_obstruction(
                    Perm.standardize(self._custom_data),
                    tplot.get_cell(Point(x, y)),
                )
            )

    def _place_point(
        self, x: int, y: int, _button: int, _modifiers: int, force_dir: int = DIR_NONE
    ) -> None:
        """Place point in a direction.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            _button (int): The mouse button clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
            force_dir (int, optional): The placement direction. Defaults to DIR_NONE.
        """
        tplot = self._current()
        ind = tplot.get_point_req_index(Point(x, y))
        if ind != TPlot.REQ_NOT_FOUND:
            self._add_tiling(
                tplot.tiling.place_point_of_gridded_permutation(
                    tplot.tiling.requirements[ind[0]][ind[1]], ind[2], force_dir
                )
            )

    def _partial_place_point(
        self, x: int, y: int, _button: int, _modifiers: int, force_dir: int = DIR_NONE
    ) -> None:
        """Partially place a point in a direction.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            _button (int): The mouse button clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
            force_dir (int, optional): The placement direction. Defaults to DIR_NONE.
        """
        tplot = self._current()
        ind = tplot.get_point_req_index(Point(x, y))
        if ind != TPlot.REQ_NOT_FOUND:
            self._add_tiling(
                tplot.tiling.partial_place_point_of_gridded_permutation(
                    tplot.tiling.requirements[ind[0]][ind[1]], ind[2], force_dir
                )
            )

    def _factor(self, x: int, y: int, _button: int, _modifiers: int) -> None:
        """Factor the clicked cell.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            _button (int): The mouse button clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
        """
        tplot = self._current()
        self._factor_from_algorithm(tplot.get_cell(Point(x, y)), Factor(tplot.tiling))

    def _factor_with_interleaving(
        self, x: int, y: int, _button: int, _modifiers: int
    ) -> None:
        """Factor the clicked cell with interleaving.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            _button (int): The mouse button clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
        """
        tplot = self._current()
        self._factor_from_algorithm(
            tplot.get_cell(Point(x, y)), FactorWithInterleaving(tplot.tiling)
        )

    def _fusion(self, x: int, y: int, _button: int, _modifiers: int, row: bool) -> None:
        """Fusion with either the clicked row or column.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            _button (int): The mouse button clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
            row (bool): Set row in fusion?
        """
        tplot = self._current()
        c, r = tplot.get_cell(Point(x, y))
        if not self._empty():
            try:
                if row:
                    n_plot = TPlot(tplot.tiling.fusion(row=r), self._w, self._h)
                else:
                    n_plot = TPlot(tplot.tiling.fusion(col=c), self._w, self._h)
                if n_plot is not None:
                    self._add_plot(n_plot)
            except (InvalidOperationError, NotImplementedError):
                pass

    def _component_fusion(
        self, x: int, y: int, _button: int, _modifiers: int, row: bool
    ) -> None:
        """Component fusion with either the clicked row or column.

        Args:
            x (int): The x coordinate of the mouse click.
            y (int): The y coordinate of the mouse click.
            _button (int): The mouse button clicked. Unused.
            _modifiers (int): If combinded with modifiers (e.g. ctrl). Unused.
            row (bool): Set row in fusion?
        """
        tplot = self._current()
        c, r = tplot.get_cell(Point(x, y))
        if not self._empty():
            try:
                if row:
                    n_plot = TPlot(
                        tplot.tiling.component_fusion(row=r), self._w, self._h
                    )
                else:
                    n_plot = TPlot(
                        tplot.tiling.component_fusion(col=c), self._w, self._h
                    )
                if n_plot is not None:
                    self._add_plot(n_plot)
            except (InvalidOperationError, NotImplementedError):
                pass


TPlotManager.register_event_type(CustomEvents.ON_EXPORT)
