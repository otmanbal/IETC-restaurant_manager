import json
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Signal, Qt


class LoginPage(QWidget):
    """
    Interface de connexion pour les utilisateurs de l'application Restaurant Manager.
    Permet de saisir un nom d'utilisateur et un mot de passe, puis vérifie les identifiants.
    """
    
    login_successful = Signal(str, bool)  # Ajout de isAdmin au signal

    def __init__(self):
        """
        Initialise la fenêtre de connexion.
        Charge les utilisateurs depuis le fichier JSON et construit un index.
        """
        super().__init__()
        self.setWindowTitle("Connexion - Restaurant Manager")
        self.setFixedSize(300, 200)
        self.users_data = self.load_users()
        self.users_index = self.create_user_index(self.users_data)
        self.init_ui()

    def init_ui(self):
        """
        Crée et organise les widgets de l'interface graphique.
        Inclut les champs pour le nom d'utilisateur et le mot de passe,
        ainsi qu'un bouton pour se connecter.
        """
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
        """
        Charge la liste des utilisateurs depuis un fichier JSON.
        Affiche un message d'erreur si le fichier est introuvable ou invalide.

        Retourne :
            list : Liste des utilisateurs chargés ou liste vide en cas d'erreur.
        """
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
        """
        Crée un index des utilisateurs pour une recherche rapide.

        Paramètres :
            users_list (list) : Liste des utilisateurs chargés depuis le fichier.

        Retourne :
            dict : Index sous forme {nom: {mot_de_passe, isAdmin}}.
        """
        # Création d’un index {nom: {mot_de_passe, isAdmin}}
        user_index = {}
        for user in users_list:
            user_index[user["nom"]] = {
                "mot_de_passe": user["mot_de_passe"],
                "isAdmin": user.get("isAdmin", False)
            }
        return user_index

    def check_credentials(self):
        """
        Vérifie les identifiants saisis dans les champs utilisateur et mot de passe.
        Émet un signal si la connexion est réussie, sinon affiche un message d'erreur.
        """
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Champs vides", "Veuillez remplir tous les champs.")
            return

        user_info = self.users_index.get(username)
        if user_info and user_info["mot_de_passe"] == password:
            self.login_successful.emit(username, user_info["isAdmin"])
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
