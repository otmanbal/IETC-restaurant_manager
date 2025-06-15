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

    def _build_ui(self):
        main = QVBoxLayout(self)
        self.service_combo = QComboBox()
        self.service_combo.addItems(["Service 1 (12h-14h)","Service 2 (15h-17h)","Service 3 (18h-20h)","Service 4 (21h-23h)"])
        main.addWidget(QLabel("Choisissez le service :"))
        main.addWidget(self.service_combo)
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("HH:mm")
        main.addWidget(QLabel("Heure de réservation :"))
        main.addWidget(self.time_edit)
        main.addWidget(QLabel(f"Choisissez l'état de : {self.windowTitle()}"), alignment=Qt.AlignCenter)

        buttons = QHBoxLayout()
        self.btn_free = QPushButton("Libre")
        self.btn_occ = QPushButton("Occupée")
        self.btn_free.clicked.connect(self.set_free)
        self.btn_occ.clicked.connect(self.show_order_widgets)
        buttons.addWidget(self.btn_free)
        buttons.addWidget(self.btn_occ)
        main.addLayout(buttons)

        self.zone = QFrame()
        self.zone.hide()
        form = QVBoxLayout(self.zone)
        self._add_items(form, "Entrées", CARTE_ENTREES, "entree_spins")
        self._add_items(form, "Plats", CARTE_PLATS, "plat_spins")
        self._add_items(form, "Desserts", CARTE_DESSERTS, "dessert_spins")

        self.label_total = QLabel("Total : 0.00 €")
        form.addWidget(self.label_total)

        self.btn_ok = QPushButton("Enregistrer la commande")
        self.btn_ok.clicked.connect(self.validate_occupied)
        form.addWidget(self.btn_ok)

        main.addWidget(self.zone)
