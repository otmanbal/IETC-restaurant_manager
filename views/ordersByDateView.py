import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


class OrdersByDateView(QWidget):
    """
    Permet d’afficher, sous forme de tableau, les commandes effectuées à une date donnée,
    avec un accès aux factures PDF si disponibles.
    """

    def __init__(self, date):
        """
        Initialise la fenêtre affichant les commandes d'une date spécifique.
        """
        super().__init__()
        self.setWindowTitle(f"Commandes du {date}")
        self.resize(600, 400)

        # Mise en page principale
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Commandes du {date}"))

        # Chargement et affichage des commandes
        self.orders = self.load_orders_for_date(date)
        self.order_table = self.create_order_table(self.orders)

        # Ajout du tableau à l'interface
        layout.addWidget(self.order_table)
        self.setLayout(layout)

    def load_orders_for_date(self, date):
        """
        Charge les commandes depuis le fichier JSON et filtre celles correspondant à la date donnée.
        """
        # Construction du chemin vers le fichier JSON des réservations
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, "database", "reservations.json")

        # Lecture du fichier JSON
        with open(json_path, "r", encoding="utf-8") as f:
            all_orders = json.load(f)

        # Filtrage des commandes par date
        return [order for order in all_orders if order.get("date") == date]

    def create_order_table(self, orders):
        """
        Crée et remplit le tableau d’affichage des commandes avec boutons de visualisation des factures.
        """
        # Initialisation du tableau avec 4 colonnes : ID, Table, Total, Facture
        table = QTableWidget(len(orders), 4)
        table.setHorizontalHeaderLabels(["ID", "Table", "Total", "Facture"])

        # Remplissage du tableau ligne par ligne
        for row, order in enumerate(orders):
            # Données textuelles
            table.setItem(row, 0, QTableWidgetItem(str(order.get("id", ""))))
            table.setItem(row, 1, QTableWidgetItem(str(order.get("table_no", ""))))
            table.setItem(row, 2, QTableWidgetItem(f"{order.get('price', 0):.2f}"))

            # Bouton de visualisation de la facture PDF
            button = self.create_invoice_button(order.get("facture"))
            table.setCellWidget(row, 3, button)

        return table

    def create_invoice_button(self, pdf_path):
        """
        Crée un bouton permettant d’ouvrir une facture PDF si le chemin est valide.
        """
        btn = QPushButton("Voir Facture")

        # Activation du bouton si le fichier existe, sinon désactivation
        if pdf_path and os.path.exists(pdf_path):
            btn.clicked.connect(lambda _, path=pdf_path: self.open_pdf(path))
        else:
            btn.setEnabled(False)

        return btn

    def open_pdf(self, file_path):
        """
        Permet d’ouvrir une facture PDF dans le lecteur de fichiers par défaut.
        """
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
