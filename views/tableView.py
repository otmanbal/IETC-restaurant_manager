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
