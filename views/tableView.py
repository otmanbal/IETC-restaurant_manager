from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PySide6.QtCore import Qt
from controllers.tableController import tableController

TABLE_SIZE_MAP = {2: (120, 60), 4: (120, 80), 6: (120, 200), 8: (120, 270)}

class tableView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Les Saveurs Orientales")
        self.setGeometry(150, 100, 1150, 650)
        self.controller = tableController(self)
        self.buttons = {}
        self._setup_ui()
        
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("Plan de salle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:30px; font-weight:600; text-decoration:underline; margin-bottom:12px;")
        layout.addWidget(title)

        grid = QGridLayout()
        layout.addLayout(grid)

        def add_table(id, row, col, rowspan, colspan, seats):
            label = f"Table {seats} places"
            btn = QPushButton(label)
            w, h = TABLE_SIZE_MAP[seats]
            btn.setFixedSize(w, h)
            btn.setStyleSheet("background-color: green;")
            btn.clicked.connect(lambda: self.controller.handle_table_click(id, label))
            self.buttons[id] = btn
            grid.addWidget(btn, row, col, rowspan, colspan, Qt.AlignCenter)

        add_table(1, 0, 0, 3, 1, 8)
        add_table(2, 0, 1, 1, 1, 4)
        add_table(3, 1, 1, 1, 1, 4)
        add_table(4, 2, 1, 1, 1, 2)
        add_table(5, 0, 2, 1, 1, 4)
        add_table(6, 1, 2, 1, 1, 4)
        add_table(7, 2, 2, 1, 1, 2)
        add_table(8, 0, 3, 2, 1, 6)
        add_table(9, 2, 3, 1, 1, 2)
