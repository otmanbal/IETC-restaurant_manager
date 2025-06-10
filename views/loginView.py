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
