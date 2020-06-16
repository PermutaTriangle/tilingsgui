
class GuiState:
    def __init__(self):
        self.shading: bool = True
        self.pretty_points: bool = True
        self.show_crossing: bool = True
        self.show_localized: bool = True
        self.highlight_touching_cell: bool = False

        self.basis_input_focus = False
        self.basis_input_read = False
        self.basis_input_string = ''

        self.cell_input_focus = False
        self.cell_input_read = False
        self.cell_input_string = ''

        self.strategy_selected = 0

        self.export = False

        self.redo = False
        self.undo = False

        self.obstruction_transivity = False
        self.row_col_seperation = False
