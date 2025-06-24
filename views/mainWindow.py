from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QStackedWidget, QWidget, QApplication,
    QSizePolicy, QMenu
)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import QSize, QPoint, QTimer

from views.tableView import tableView
from views.adminView import AdminView
from views.financeView import FinanceView
from views.loginView import LoginPage
from views.rapportView import RapportView


class mainWindow(QMainWindow):
    """
    Fenêtre principale de l'application restaurant, avec une barre d'outils
    permettant la navigation entre les différentes vues (tables, admin, finance).
    """

    def __init__(self, username=None, is_admin=False):
        """
        Initialise la fenêtre principale avec les vues nécessaires et la barre de navigation.
        """
        super().__init__()
        self.setWindowTitle(f"Restaurant Manager - Connecté en tant que {username}")
        self.resize(800, 600)

        self.username = username
        self.is_admin = is_admin

        # Création de la barre d'outils de navigation
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        # Création du conteneur de vues (stack central)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialisation des différentes pages/vues
        self.page_tables = tableView()
        self.page_admin = AdminView()
        self.page_finance_rapport = RapportView()
        self.page_finance = FinanceView()

        # Ajout des vues au stack avec un index associé
        self.stack.addWidget(self.page_tables)            # index 0
        self.stack.addWidget(self.page_admin)             # index 1
        self.stack.addWidget(self.page_finance_rapport)   # index 2
        self.stack.addWidget(self.page_finance)           # index 3

        # Définition des actions de navigation
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

        # Restriction des boutons admin si l'utilisateur n'est pas administrateur
        if not self.is_admin:
            self.action_admin.setEnabled(False)
            self.action_finance.setEnabled(False)
            self.action_rapport_finance.setEnabled(False)

        # Espace vide pour pousser les éléments à droite
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        # Ajout de l'icône de profil à la barre d'outils
        profile_pixmap = QPixmap("ressources/images/pdp.webp")
        profile_icon = QIcon(profile_pixmap.scaled(40, 40))
        action_profil = QAction(profile_icon, "", self)
        action_profil.setToolTip("Profil")
        toolbar.addAction(action_profil)
        toolbar.setIconSize(QSize(40, 40))

        # Menu contextuel pour le bouton profil
        self.profile_menu = QMenu(self)
        self.profile_menu.addAction("Se déconnecter", self.logout)
        action_profil.triggered.connect(self.show_profile_menu)

    def show_profile_menu(self):
        """
        Affiche le menu contextuel du profil utilisateur sous l'icône.
        """
        pos = self.mapToGlobal(QPoint(self.width() - 60, 50))
        self.profile_menu.exec(pos)

    def logout(self):
        """
        Déconnecte l'utilisateur et affiche la page de connexion.
        """
        self.login_page = LoginPage()
        self.login_page.login_successful.connect(self.reopen_main_window)
        self.login_page.show()

        # Fermer la fenêtre principale dès que possible après affichage de la page de login
        QTimer.singleShot(0, self.close)

    def reopen_main_window(self, username, is_admin):
        """
        Rouvre une nouvelle instance de la fenêtre principale avec les nouveaux identifiants.
        """
        self.login_page.close()
        self.new_window = mainWindow(username=username, is_admin=is_admin)
        self.new_window.show()
