"""
Point d’entrée principal de l’application de gestion du restaurant.
Affiche la page de connexion, puis lance l’interface principale après authentification.
"""

from PySide6.QtWidgets import QApplication
from views.loginView import LoginPage
from views.mainWindow import mainWindow  # À renommer MainWindow si c’est une classe
import sys


def main():
    """
    Initialise l’application Qt, affiche la page de connexion,
    et ouvre la fenêtre principale après connexion réussie.
    """
    app = QApplication(sys.argv)

import sys
from PySide6.QtWidgets import QApplication

from views.loginView import LoginPage
from views.mainWindow import mainWindow


def main():
    app = QApplication(sys.argv)
    

    login = LoginPage()
    login.show()

    def handle_login(username, is_admin):

        """
        Ferme la page de connexion et ouvre la fenêtre principale
        après une authentification réussie.
        """
        login.close()
        main_window = mainWindow()
        main_window.show()

    login.login_successful.connect(handle_login)

        login.close()
        main_window = mainWindow(username=username, is_admin=is_admin)
        main_window.show()
        
    login.login_successful.connect(handle_login)
    

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
