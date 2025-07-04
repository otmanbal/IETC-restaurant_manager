from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QSpinBox, QComboBox, QTimeEdit, QLineEdit, QScrollArea, QWidget
from PySide6.QtCore import Qt, QTime, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from datetime import datetime
from models.menu import CARTE_ENTREES, CARTE_PLATS, CARTE_DESSERTS

class tableDialog(QDialog):
    """
    Fenêtre de dialogue pour gérer l'état d'une table et enregistrer une commande.
    Elle permet de saisir les informations du client, l'heure de réservation,
    le service, et les plats commandés.
    """
    def __init__(self, table_label: str, previous_order=None, parent=None):
        """
        Initialise la boîte de dialogue pour une table donnée.

        :param table_label: Le nom ou numéro de la table (ex: "Table 1")
        :param previous_order: Dictionnaire d'une commande précédente à recharger (facultatif)
        :param parent: Le parent Qt (facultatif)
        """
        super().__init__(parent)
        self.setWindowTitle(table_label)
        self.setFixedSize(300, 750)
        self.occupied = None
        self.previous_order = previous_order
        self.order = {"entrees": [], "plats": [], "desserts": []}
        self.build_ui()
        self.populate_previous_order()

    def build_ui(self):
        """
        Construit l'interface utilisateur de la boîte de dialogue :
        informations client, choix du service, état de la table, et commande.
        """
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        scroll_area.setWidget(container)
        
        main = QVBoxLayout(self)

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        phone_validator = QRegularExpressionValidator(QRegularExpression(r"\d+"))
        self.phone_input.setValidator(phone_validator)
        
        main.addWidget(QLabel("Prénom :"))
        main.addWidget(self.first_name_input)
        main.addWidget(QLabel("Nom :"))
        main.addWidget(self.last_name_input)
        main.addWidget(QLabel("Numéro de téléphone :"))
        main.addWidget(self.phone_input)
        
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

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

    def add_items(self, layout, title, items, attr_name):
        """
        Ajoute dynamiquement les articles à commander (entrées, plats ou desserts).

        :param layout: Le layout dans lequel les éléments seront ajoutés
        :param title: Le titre de la section (ex: "Plats")
        :param items: Liste d'objets représentant les mets
        :param attr_name: Nom de l'attribut dans lequel stocker les spinbox
        """
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
        """
        Recharge une commande précédente si elle est fournie.
        Remplit automatiquement les quantités dans les spinbox.
        """
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
        """
        Affiche les champs de commande lorsque la table est marquée comme occupée.
        """
        self.zone.show()
        
    def update_total(self):
        """
        Met à jour le total de la commande en fonction des quantités sélectionnées.
        """
        total = 0.0
        for spin in self.entree_spins + self.plat_spins + self.dessert_spins:
            total += spin.item.price * spin.value()
        self.label_total.setText(f"Total : {total:.2f} €")

    def validate_occupied(self):
        """
        Valide la table comme occupée, enregistre les données saisies et accepte la boîte de dialogue.
        """
        self.occupied = True

        def collect(spins):
            return [
                {"name": spin.item.name, "price": spin.item.price, "qty": spin.value()}
                for spin in spins if spin.value() > 0
            ]

        self.order = {
            "prenom": self.first_name_input.text(),
            "nom": self.last_name_input.text(),
            "telephone": self.phone_input.text(),
            "entrees": collect(self.entree_spins),
            "plats": collect(self.plat_spins),
            "desserts": collect(self.dessert_spins)
        }
        self.accept()
        selected_service = self.service_combo.currentText()
        hour_str = self.time_edit.time().toString("HH:mm")
        self.order["reservation_time"] = f"{selected_service} - {hour_str}"
        self.order["datetime_iso"] = datetime.now().isoformat()

    def set_free(self):
        """
        Marque la table comme libre et ferme la boîte de dialogue.
        """
        self.occupied = False
        self.accept()
