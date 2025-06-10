import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

class OrdersByDateView(QWidget):
    def __init__(self, date):
        super().__init__()
        self.setWindowTitle(f"Commandes du {date}")
        self.resize(600, 400)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Commandes du {date}"))

        # Charger les réservations depuis le fichier JSON
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        JSON_PATH = os.path.join(BASE_DIR, "database", "reservations.json")

        with open(JSON_PATH, "r") as f:
             all_orders = json.load(f)


        # Filtrer les réservations du jour
        orders_of_the_day = []
        for order in all_orders:
            if order["date"] == date:
                orders_of_the_day.append(order)

        self.orders = orders_of_the_day

        # Créer le tableau
        self.order_table = QTableWidget()
        self.order_table.setRowCount(len(self.orders))
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(["ID", "Table", "Total", "Facture"])

        for row, order in enumerate(self.orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
            self.order_table.setItem(row, 1, QTableWidgetItem(str(order["table_no"])))
            self.order_table.setItem(row, 2, QTableWidgetItem(f"{order['price']:.2f}"))

            btn = QPushButton("Voir Facture")
            if "facture" in order and os.path.exists(order["facture"]):
                pdf_path = order["facture"]
                btn.clicked.connect(lambda _, pdf=pdf_path: self.open_pdf(pdf))
            else:
                btn.setEnabled(False)

            self.order_table.setCellWidget(row, 3, btn)

        layout.addWidget(self.order_table)
        self.setLayout(layout)

    def open_pdf(self, file_path):
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
