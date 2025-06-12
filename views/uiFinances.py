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
