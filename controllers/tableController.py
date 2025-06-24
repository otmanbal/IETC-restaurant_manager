from views.tableDialog import tableDialog
from models.persist import get_last_order, add_order, close_table
from models.order_logic import calculer_total

class tableController:
    """
    Contrôleur responsable de la gestion des interactions avec les tables.
    Il coordonne l'ouverture de la boîte de dialogue, l'enregistrement ou la libération des tables,
    et la mise à jour de l'interface utilisateur.
    """
    def __init__(self, main_window):
        """
        Initialise le contrôleur avec une référence à la fenêtre principale.

        :param main_window: L'instance de la vue principale (tableView)
        """
        self.main_window = main_window

    def handle_table_click(self, table_id: int, label: str):
        """
        Gère le clic sur une table. Ouvre une boîte de dialogue pour la table sélectionnée,
        récupère la commande précédente si disponible, et met à jour l'état de la table selon l'action de l'utilisateur.

        :param table_id: Identifiant de la table
        :param label: Texte affiché sur le bouton de la table (ex: "Table 4 places")
        """
        previous_order = get_last_order(table_id)
        dialog = tableDialog(label, previous_order=previous_order, parent=self.main_window)
        if dialog.exec():
            btn = self.main_window.buttons[table_id]
            if dialog.occupied:
                add_order(table_id, dialog.order)
                total = calculer_total(dialog.order)
                btn.setStyleSheet("background-color: red;")
                btn.setText(f"{label}\nTotal : {total:.2f} €")
            else:
                close_table(table_id)
                btn.setStyleSheet("background-color: green;")
                btn.setText(label)
