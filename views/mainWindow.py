from PySide6.QtWidgets import ( QMainWindow, QToolBar, QStackedWidget,
    QWidget, QSizePolicy
)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import QSize, QTimer, QTime
from views.menuView import MenuView
from views.financeView import FinanceView
from views.adminView import AdminView
from views.tableView import tableView


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Manager")
        self.resize(800, 600)

        # Navigation
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        # Stack central
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.page_tables = tableView()
        self.page_menu = MenuView()
        self.page_finance = FinanceView()
        self.page_profil = AdminView()

        self.stack.addWidget(self.page_tables)  
        self.stack.addWidget(self.page_menu)     
        self.stack.addWidget(self.page_finance)  
        self.stack.addWidget(self.page_profil)   
