from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QSpinBox, QComboBox, QTimeEdit
from PySide6.QtCore import Qt, QTime
from datetime import datetime
from models.menu import CARTE_ENTREES, CARTE_PLATS, CARTE_DESSERTS

class tableDialog(QDialog):
    def __init__(self, table_label: str, previous_order=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(table_label)
        self.occupied = None
        self.previous_order = previous_order
        self.order = {"entrees": [], "plats": [], "desserts": []}
        self._build_ui()
        self._populate_previous_order()
