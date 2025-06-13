from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from models.gestionFinances import ajouterEntree, chargerDonnees
from models.rapportFinances import generateReport
from datetime import datetime
import sys


class InterfaceFinance(QWidget):
    """
        Constructeur de la fenêtre principale : initialise la fenêtre,
        définit son titre et sa taille, puis lance la création de l’interface utilisateur.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des finances")
        self.setGeometry(200, 200, 800, 4600)
        self.init_ui()


    def init_ui(self):
        """
            Initialise l’interface graphique pour la saisie et la gestion des données financières :
            champs de saisie, boutons d’action, et tableau d’affichage des données.
        """
        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")

        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Total facture")

        self.type_input = QComboBox()
        self.type_input.addItems(["virement", "cache"])

        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_ajouter.clicked.connect(self.ajouterDonnee)

        self.btn_rafraichir = QPushButton("Afficher les données")
        self.btn_rafraichir.clicked.connect(self.afficherDonnees)

        self.btn_rapport = QPushButton("Générer le rapport")
        self.btn_rapport.clicked.connect(self.generateReport)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Paiement", "Total"])

        layout.addWidget(QLabel("Ajouter une entrée financière :"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.total_input)
        layout.addWidget(self.type_input)
        layout.addWidget(self.btn_ajouter)
        layout.addWidget(self.btn_rafraichir)
        layout.addWidget(self.btn_rapport)
        layout.addWidget(self.table)

        self.setLayout(layout)

    
    def ajouterDonnee(self):
        """
            Récupère les données saisies, les valide et les enregistre puis
            affiche un message de succès ou une erreur selon le cas,
            puis met à jour l’affichage de la table.
        """
        try:
            id_val = int(self.id_input.text())
            total = float(self.total_input.text())
            type_paiement = self.type_input.currentText()
            date = datetime.today().strftime('%Y-%m-%d')

            ajouterEntree(id_val, date, type_paiement, total)
            QMessageBox.information(self, "Succès", "Donnée ajoutée avec succès.")
            self.id_input.clear()
            self.total_input.clear()
            self.afficherDonnees()
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Vérifiez les valeurs saisies.")


    def afficherDonnees(self):
        """
            Charge les données financières et les affiche ligne par ligne dans le tableau de l’interface.
        """
        donnees = chargerDonnees()
        self.table.setRowCount(len(donnees))
        for row, entree in enumerate(donnees):
            self.table.setItem(row, 0, QTableWidgetItem(str(entree["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(entree["date"]))
            self.table.setItem(row, 2, QTableWidgetItem(entree["type_paiement"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(entree["total_facture"])))
