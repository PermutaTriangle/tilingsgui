class GuiState:
    def __init__(self):
        self.shading: bool = True
        self.pretty_points: bool = True
        self.show_crossing: bool = True
        self.show_localized: bool = True
        self.highlight_touching_cell: bool = False

        self.basis_input_focus = False
        self.basis_input_read = False
        self.basis_input_string = ""

        self.cell_input_focus = False
        self.cell_input_read = False
        self.cell_input_string = ""

        self.strategy_selected = 0

        self.export = False

        self.redo = False
        self.undo = False

        self.obstruction_transivity = False
        self.row_col_seperation = False

    def toggle_shading(self):
        self.shading = not self.shading
        print(f"toggle shading: {self.shading}")

    def toggle_pretty_points(self):
        self.pretty_points = not self.pretty_points
        print(f"toggle pretty_points: {self.pretty_points}")

    def toggle_show_crossing(self):
        self.show_crossing = not self.show_crossing
        print(f"toggle show_crossing: {self.show_crossing}")

    def toggle_show_localized(self):
        self.show_localized = not self.show_localized
        print(f"toggle show_localized: {self.show_localized}")

    def toggle_highlight_touching_cell(self):
        self.highlight_touching_cell = not self.highlight_touching_cell
        print(f"toggle highlight_touching_cell: {self.highlight_touching_cell}")

    def set_strategy(self, i):
        self.strategy_selected = i
        print(f"strategy_selected: {self.strategy_selected}")

    def set_export(self):
        self.export = True
        print(f"export: {self.export}")

    def set_redo(self):
        self.redo = True
        print(f"redo: {self.redo}")

    def set_undo(self):
        self.undo = True
        print(f"undo: {self.undo}")

    def set_obstruction_transivity(self):
        self.obstruction_transivity = True
        print(f"obstruction_transivity: {self.obstruction_transivity}")

    def set_row_col_seperation(self):
        self.row_col_seperation = True
        print(f"row_col_seperation: {self.row_col_seperation}")
