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

        Paramètres :
        - username : nom d'utilisateur connecté
        - is_admin : booléen indiquant si l'utilisateur est un administrateur
        """
        login.close()
        main_window = mainWindow()
        main_window.show()

    login.login_successful.connect(handle_login)    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
