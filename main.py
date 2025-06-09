import sys
from PySide6.QtWidgets import QApplication

from controllers.TableController import TableController
from views.financeView import FinanceView
from views.loginView import LoginPage
from views.mainWindow import mainWindow
from views.tableView import TableView


def main():
    app = QApplication(sys.argv)
    
    login = LoginPage()
    login.show()

    def handle_login(username, is_admin):
        login.close()
        main_window = mainWindow()
        main_window.show()
        
    login.login_successful.connect(handle_login)
    
    sys.exit(app.exec())


if __name__ == "__main__":

    main()

