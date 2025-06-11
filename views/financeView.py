import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractScrollArea, QScrollArea, QPushButton, QTabWidget, QMessageBox
)
from .ordersByDateView import OrdersByDateView

from collections import defaultdict
from uiFinances import InterfaceFinance
from controllers.rapportFinances import generateReport
from controllers.gestionFinances import chargerDonnees

class FinanceView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance View")

        layout = QVBoxLayout(self)

        # Tableau du haut : paiements
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(5)
        self.payment_table.setHorizontalHeaderLabels(["ID", "Table No.", "Date", "Payment Type", "Price"])
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payment_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


        # Scroll pour le tableau du haut
        payment_scroll = QScrollArea()
        payment_scroll.setWidgetResizable(True)
        payment_scroll.setWidget(self.payment_table)
        row_height = self.payment_table.verticalHeader().defaultSectionSize()
        header_height = self.payment_table.horizontalHeader().height()
        payment_scroll.setFixedHeight(row_height * 10 + header_height + 10)


        # Tableau du bas : totaux journaliers
        self.daily_total_table = QTableWidget()
        self.daily_total_table.setColumnCount(3)
        self.daily_total_table.setHorizontalHeaderLabels(["ID", "Date", "Daily Total"])
        self.daily_total_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.daily_total_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Connexion du clic pour afficher les commandes du jour
        self.daily_total_table.cellClicked.connect(self.show_daily_orders)

        # Ajout au layout
        layout.addWidget(QLabel("Payment Records"))
        layout.addWidget(payment_scroll)
        layout.addWidget(QLabel("Daily Totals"))
        layout.addWidget(self.daily_total_table)
        self.setLayout(layout)

    def populate_payments(self, payment_list):
        self.payment_table.setRowCount(0)
        for record in payment_list:
            row = self.payment_table.rowCount()
            self.payment_table.insertRow(row)
            self.payment_table.setItem(row, 0, QTableWidgetItem(str(record["id"])))
            self.payment_table.setItem(row, 1, QTableWidgetItem(str(record["table_no"])))
            self.payment_table.setItem(row, 2, QTableWidgetItem(record["date"]))
            self.payment_table.setItem(row, 3, QTableWidgetItem(record["payment_type"]))
            self.payment_table.setItem(row, 4, QTableWidgetItem(f"{record['price']:.2f}"))

    def populate_daily_totals(self, totals_list):
        self.daily_total_table.setRowCount(0)
        for record in totals_list:
            row = self.daily_total_table.rowCount()
            self.daily_total_table.insertRow(row)
            self.daily_total_table.setItem(row, 0, QTableWidgetItem(str(record["id"])))
            self.daily_total_table.setItem(row, 1, QTableWidgetItem(record["date"]))
            self.daily_total_table.setItem(row, 2, QTableWidgetItem(f"{record['total']:.2f}"))

    def show_daily_orders(self, row, column):
        date_item = self.daily_total_table.item(row, 1)
        if not date_item:
            return
        selected_date = date_item.text()
        self.order_view = OrdersByDateView(selected_date)
        self.order_view.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application de gestion financière du restaurant")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()

    def init_ui(self):
        """
            Initialise l’interface graphique : crée un système d’onglets avec les vues de finance,
            ajoute un bouton pour générer un rapport PDF, et affiche les données financières.
        """
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        self.interface_finance = InterfaceFinance()
        self.tabs.addTab(self.interface_finance, "Gestion des paiements")

        self.finance_view = FinanceView()
        self.tabs.addTab(self.finance_view, "Vue des finances")

        self.btn_imprimer = QPushButton("Imprimer le rapport PDF")
        self.btn_imprimer.clicked.connect(self.generateReport)

        layout.addWidget(self.tabs)
        layout.addWidget(self.btn_imprimer)

        self.setLayout(layout)
        self.rafraichirTables()


    def generateReport(self):
        """
            Génère un rapport PDF, affiche un message de confirmation,
            puis rafraîchit les tables affichées dans l’interface.
        """
        generateReport()
        QMessageBox.information(self, "Succès", "Le rapport PDF a été généré.")
        self.rafraichirTables() 
