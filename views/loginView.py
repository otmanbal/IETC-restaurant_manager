import json
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Signal, Qt


class LoginPage(QWidget):
    login_successful = Signal(str, bool)  # Ajout de isAdmin au signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion - Restaurant Manager")
        self.setFixedSize(300, 200)
        self.users_data = self.load_users()
        self.users_index = self.create_user_index(self.users_data)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_info = QLabel("Veuillez vous connecter")
        self.label_info.setAlignment(Qt.AlignCenter)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Nom d'utilisateur")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Mot de passe")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Se connecter")
        self.btn_login.clicked.connect(self.check_credentials)

        layout.addWidget(self.label_info)
        layout.addWidget(self.input_username)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)
        
    def load_users(self):
        file_path = Path(__file__).parent.parent / "database" / "employes.json"
        if not os.path.exists(file_path):
            QMessageBox.critical(self, "Erreur", "Fichier des utilisateurs introuvable.")
            return []

        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
                return data.get("users", [])
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Erreur", "Erreur de lecture du fichier JSON.")
            return []

    def create_user_index(self, users_list):
        # Création d’un index {nom: {mot_de_passe, isAdmin}}
        user_index = {}
        for user in users_list:
            user_index[user["nom"]] = {
                "mot_de_passe": user["mot_de_passe"],
                "isAdmin": user.get("isAdmin", False)
            }
        return user_index
