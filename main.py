import sys
from PySide6.QtWidgets import QApplication

from views.loginView import LoginPage
from views.mainWindow import mainWindow


def main():
    app = QApplication(sys.argv)
    
    login = LoginPage()
    login.show()

    def handle_login(username, is_admin):
        login.close()
        main_window = mainWindow(username=username, is_admin=is_admin)
        main_window.show()
        
    login.login_successful.connect(handle_login)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
