import sys
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractScrollArea, QScrollArea
)
from .ordersByDateView import OrdersByDateView
from collections import defaultdict
from controllers.uiFinances import InterfaceFinance
from controllers.rapportFinances import generateReport
from controllers.gestionFinances import chargerDonnees


class FinanceView(QWidget):
    """
    Interface graphique affichant les paiements enregistrés et les totaux journaliers,
    avec possibilité de consulter les commandes d’un jour donné.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance View")

        layout = QVBoxLayout(self)

        # Tableau des paiements
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(5)
        self.payment_table.setHorizontalHeaderLabels(["ID", "Table No.", "Date", "Payment Type", "Price"])
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payment_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Scroll pour le tableau des paiements
        payment_scroll = QScrollArea()
        payment_scroll.setWidgetResizable(True)
        payment_scroll.setWidget(self.payment_table)
        row_height = self.payment_table.verticalHeader().defaultSectionSize()
        header_height = self.payment_table.horizontalHeader().height()
        payment_scroll.setFixedHeight(row_height * 10 + header_height + 10)

        # Tableau des totaux journaliers
        self.daily_total_table = QTableWidget()
        self.daily_total_table.setColumnCount(3)
        self.daily_total_table.setHorizontalHeaderLabels(["ID", "Date", "Daily Total"])
        self.daily_total_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.daily_total_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Interaction : clic sur une ligne pour afficher les commandes du jour
        self.daily_total_table.cellClicked.connect(self.show_daily_orders)

        # Ajout des widgets à l’interface
        layout.addWidget(QLabel("Payment Records"))
        layout.addWidget(payment_scroll)
        layout.addWidget(QLabel("Daily Totals"))
        layout.addWidget(self.daily_total_table)
        self.setLayout(layout)
        # Charger les réservations
        try:
            with open("database/reservations.json", "r") as f:
                all_reservations = json.load(f)
        except FileNotFoundError:
            all_reservations = []

        # Calculer les totaux journaliers
        daily_totals = {}
        for record in all_reservations:
            date = record["date"]
            daily_totals[date] = daily_totals.get(date, 0) + record["price"]

        daily_totals_list = []
        for i, (date, total) in enumerate(daily_totals.items(), start=1):
            daily_totals_list.append({"id": i, "date": date, "total": total})

        # Injecter les données dans la page finance
        self.populate_payments(all_reservations)
        self.populate_daily_totals(daily_totals_list)
        
    def populate_payments(self, payment_list):
        """
        Remplit le tableau des paiements avec une liste d’enregistrements de paiement.
        """
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
        """
        Remplit le tableau des totaux journaliers avec les montants totaux par date.
        """
        self.daily_total_table.setRowCount(0)
        for record in totals_list:
            row = self.daily_total_table.rowCount()
            self.daily_total_table.insertRow(row)
            self.daily_total_table.setItem(row, 0, QTableWidgetItem(str(record["id"])))
            self.daily_total_table.setItem(row, 1, QTableWidgetItem(record["date"]))
            self.daily_total_table.setItem(row, 2, QTableWidgetItem(f"{record['total']:.2f}"))

    def show_daily_orders(self, row, column):
        """
        Affiche une nouvelle fenêtre contenant les commandes du jour sélectionné.
        """
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


    def rafraichirTables(self):
        """
            Recharge les données financières depuis la source de données,
            met à jour l’affichage des paiements individuels dans la vue finance,
            puis calcule et affiche le total des paiements par jour.
        """
        donnees = chargerDonnees()
        self.finance_view.populate_payments([
            {
                "id": d["id"],
                "table_no": "-",  
                "date": d["date"],
                "payment_type": d["type_paiement"],
                "price": d["total_facture"]
            }
            for d in donnees
        ])

        total_par_jour = defaultdict(float)
        for d in donnees:
            total_par_jour[d["date"]] += d["total_facture"]

        daily_total_list = [
            {"id": i+1, "date": date, "total": total}
            for i, (date, total) in enumerate(total_par_jour.items())
        ]

        self.finance_view.populate_daily_totals(daily_total_list)

