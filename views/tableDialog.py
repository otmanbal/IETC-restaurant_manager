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
        self.build_ui()
        self.populate_previous_order()

    def build_ui(self):
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
        self.add_items(form, "Entrées", CARTE_ENTREES, "entree_spins")
        self.add_items(form, "Plats", CARTE_PLATS, "plat_spins")
        self.add_items(form, "Desserts", CARTE_DESSERTS, "dessert_spins")

        self.label_total = QLabel("Total : 0.00 €")
        form.addWidget(self.label_total)

        self.btn_ok = QPushButton("Enregistrer la commande")
        self.btn_ok.clicked.connect(self.validate_occupied)
        form.addWidget(self.btn_ok)

        main.addWidget(self.zone)

    def add_items(self, layout, title, items, attr_name):
        layout.addWidget(QLabel(title))
        spins = []
        for item in items:
            line = QHBoxLayout()
            label = QLabel(str(item))
            spin = QSpinBox()
            spin.setRange(0, 99)
            spin.item = item
            spin.valueChanged.connect(self.update_total)
            line.addWidget(label)
            line.addWidget(spin)
            layout.addLayout(line)
            spins.append(spin)
        setattr(self, attr_name, spins)

    def populate_previous_order(self):
        if not self.previous_order:
            return

        def restore(spins, key):
            items = {item["name"]: item["qty"] for item in self.previous_order.get(key, [])}
            for spin in spins:
                if spin.item.name in items:
                    spin.setValue(items[spin.item.name])

        restore(self.entree_spins, "entrees")
        restore(self.plat_spins, "plats")
        restore(self.dessert_spins, "desserts")

    def show_order_widgets(self):
        self.zone.show()
        
    def update_total(self):
        total = 0.0
        for spin in self.entree_spins + self.plat_spins + self.dessert_spins:
            total += spin.item.price * spin.value()
        self.label_total.setText(f"Total : {total:.2f} €")
        
