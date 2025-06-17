from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QStackedWidget, QWidget, QApplication,
    QSizePolicy, QMenu
)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import QSize, QPoint, QTimer

from controllers.uiFinances import InterfaceFinance
from views.menuView import MenuView
from views.financeView import FinanceSummaryView
from views.tableView import tableView
from views.adminView import AdminView
from views.financeView import FinanceView
from views.loginView import LoginPage


class mainWindow(QMainWindow):
    def __init__(self, username=None, is_admin=False):
        super().__init__()
        self.setWindowTitle(f"Restaurant Manager - Connecté en tant que {username}")
        self.resize(800, 600)

        self.username = username
        self.is_admin = is_admin

        # Navigation
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        # Stack central
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.page_tables = tableView()
        self.page_admin = AdminView()
        self.page_finance_rapport = InterfaceFinance()
        self.page_finance = FinanceView()

        self.stack.addWidget(self.page_tables)    # index 0
        self.stack.addWidget(self.page_admin)     # index 1
        self.stack.addWidget(self.page_finance_rapport)   # index 2
        self.stack.addWidget(self.page_finance)   # index 3

        # Actions navigation
        self.action_tables = QAction("Tables", self)
        self.action_tables.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        toolbar.addAction(self.action_tables)

        self.action_admin = QAction("Admin", self)
        self.action_admin.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        toolbar.addAction(self.action_admin)

        self.action_rapport_finance = QAction("Rapport Finance", self)
        self.action_rapport_finance.triggered.connect(lambda: self.stack.setCurrentIndex(2))
        toolbar.addAction(self.action_rapport_finance)

        self.action_finance = QAction("Finance", self)
        self.action_finance.triggered.connect(lambda: self.stack.setCurrentIndex(3))
        toolbar.addAction(self.action_finance)

        # Restriction des actions si non admin
        if not self.is_admin:
            self.action_admin.setEnabled(False)
            self.action_finance.setEnabled(False)
            self.action_rapport_finance.setEnabled(False)

        # Spacer pour pousser le profil à droite
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        # Icône de profil avec menu
        profile_pixmap = QPixmap("ressources/images/pdp.webp")
        profile_icon = QIcon(profile_pixmap.scaled(40, 40))
        action_profil = QAction(profile_icon, "", self)
        action_profil.setToolTip("Profil")
        toolbar.addAction(action_profil)
        toolbar.setIconSize(QSize(40, 40))
        
        # Menu contextuel pour profil
        self.profile_menu = QMenu(self)
        self.profile_menu.addAction("Se déconnecter", self.logout)
        action_profil.triggered.connect(self.show_profile_menu)

    def show_profile_menu(self):
        pos = self.mapToGlobal(QPoint(self.width() - 60, 50))
        self.profile_menu.exec(pos)

    def logout(self):
        self.login_page = LoginPage()
        self.login_page.login_successful.connect(self.reopen_main_window)
        self.login_page.show()

        QTimer.singleShot(0, self.close)

    def reopen_main_window(self, username, is_admin):
        self.login_page.close()
        self.new_window = mainWindow(username=username, is_admin=is_admin)
        self.new_window.show()
