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
