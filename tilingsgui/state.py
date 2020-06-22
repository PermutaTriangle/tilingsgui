class GuiState:
    def __init__(self):
        self.shading: bool = True
        self.pretty_points: bool = True
        self.show_crossing: bool = True
        self.show_localized: bool = True
        self.highlight_touching_cell: bool = False

        self.strategy_selected = 0

        self.has_selected_pnt = False
        self.selected_points = tuple()
        self.point_move_bounds = tuple()
        self.move_type = 0

    def init_move_state(self):
        self.has_selected_pnt = False
        self.selected_points = tuple()
        self.point_move_bounds = tuple()
        self.move_type = 0

    def toggle_shading(self):
        self.shading = not self.shading

    def toggle_pretty_points(self):
        self.pretty_points = not self.pretty_points

    def toggle_show_crossing(self):
        self.show_crossing = not self.show_crossing

    def toggle_show_localized(self):
        self.show_localized = not self.show_localized

    def toggle_highlight_touching_cell(self):
        self.highlight_touching_cell = not self.highlight_touching_cell

    def set_strategy(self, i):
        self.strategy_selected = i
