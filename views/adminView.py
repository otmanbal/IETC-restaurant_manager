from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QMessageBox
)

class AdminView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vue Admin - Gestion des employés")
        layout = QVBoxLayout()

        # Groupe : Statistiques globales
        stats_box = QGroupBox("Statistiques des employés")
        stats_layout = QVBoxLayout()
        self.label_total_orders = QLabel("Total des commandes : ...")
        self.label_best_employee = QLabel("Meilleur employé : ...")
        stats_layout.addWidget(self.label_total_orders)
        stats_layout.addWidget(self.label_best_employee)
        stats_box.setLayout(stats_layout)

        # Groupe : Tableau employés
        crud_box = QGroupBox("Gestion des employés")
        crud_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Poste", "Statut"])
        crud_layout.addWidget(self.table)

        # Boutons CRUD
        buttons = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter")
        self.btn_edit = QPushButton("Modifier")
        self.btn_delete = QPushButton("Supprimer")
        buttons.addWidget(self.btn_add)
        buttons.addWidget(self.btn_edit)
        buttons.addWidget(self.btn_delete)
        crud_layout.addLayout(buttons)

        crud_box.setLayout(crud_layout)

        # Ajout au layout principal
        layout.addWidget(stats_box)
        layout.addWidget(crud_box)
        self.setLayout(layout)

        # Connexions (à compléter avec les fonctions)
        self.btn_add.clicked.connect(self.add_employee)
        self.btn_edit.clicked.connect(self.edit_employee)
        self.btn_delete.clicked.connect(self.delete_employee)

        self.load_employees()

        def load_employees(self):
        import json
        from pathlib import Path

        file_path = Path(__file__).parent.parent / "database" / "employes.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = data.get("users", [])
                self.table.setRowCount(len(users))
                for row, user in enumerate(users):
                    self.table.setItem(row, 0, QTableWidgetItem(str(user.get("id", ""))))
                    self.table.setItem(row, 1, QTableWidgetItem(user.get("nom", "")))
                    self.table.setItem(row, 2, QTableWidgetItem("Administrateur" if user.get("isAdmin") else "Employé"))
                    self.table.setItem(row, 3, QTableWidgetItem("Actif"))  # ou autre statut par défaut
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les employés : {e}")

    def add_employee(self):
        QMessageBox.information(self, "Ajouter", "Fonction 'Ajouter' à implémenter")

    def edit_employee(self):
        QMessageBox.information(self, "Modifier", "Fonction 'Modifier' à implémenter")

    def delete_employee(self):
        QMessageBox.information(self, "Supprimer", "Fonction 'Supprimer' à implémenter")

