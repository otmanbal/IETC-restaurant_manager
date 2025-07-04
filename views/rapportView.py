import sys
from collections import defaultdict
from PySide6.QtWidgets import ( # type: ignore
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from controllers.gestionFinances import ajouterEntree, chargerDonnees, genererNumTva
from controllers.rapportFinances import generateReport
from datetime import datetime
from views.financeView import FinanceView

class RapportView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des finances")
        self.setGeometry(200, 200, 800, 4600)

        #self.tabs = QTabWidget() # type: ignore

        layout = QVBoxLayout()

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
        self.table.setHorizontalHeaderLabels(["Num TVA", "Date", "Paiement", "Total"])

        layout.addWidget(QLabel("Ajouter une entrée financière :"))
        layout.addWidget(self.total_input)
        layout.addWidget(self.type_input)
        layout.addWidget(self.btn_ajouter)
        layout.addWidget(self.btn_rafraichir)
        layout.addWidget(self.btn_rapport)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.finance_view = FinanceView()

        self.btn_imprimer = QPushButton("Imprimer le rapport PDF")
        self.btn_imprimer.clicked.connect(self.generateReport)

        layout.addWidget(self.btn_imprimer)

        self.setLayout(layout)
        self.rafraichirTables()


    def ajouterDonnee(self):
        """
            Récupère les données saisies, les valide et les enregistre puis
            affiche un message de succès ou une erreur selon le cas,
            puis met à jour l’affichage de la table.
        """
        try:
            id = genererNumTva()
            total = float(self.total_input.text())
            type_paiement = self.type_input.currentText()
            date = datetime.today().strftime('%Y-%m-%d')

            ajouterEntree(id, date, type_paiement, total)
            QMessageBox.information(self, "Succès", f"Donnée ajoutée avec succès.\nNum TVA: {id}")
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
            self.table.setItem(row, 0, QTableWidgetItem(str(entree["Num TVA"])))
            self.table.setItem(row, 1, QTableWidgetItem(entree["date"]))
            self.table.setItem(row, 2, QTableWidgetItem(entree["type_paiement"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(entree["total_facture"])))

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
                "id": "id",
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
