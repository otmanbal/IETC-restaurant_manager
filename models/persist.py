import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

FILE = Path(__file__).parent.parent / "database" / "orders.json"



def read_orders() -> List[Dict[str, Any]]:
    """
    Lit les commandes depuis le fichier JSON s'il existe.

    :return: Liste de dictionnaires représentant les commandes.
    """
    if FILE.exists():
        with FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def write_orders(data: List[Dict[str, Any]]) -> None:
    """
    Écrit les données de commande dans le fichier JSON.

    :param data: Liste de commandes à enregistrer.
    """
    with FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_order(table_id: int, order: Dict[str, Any]) -> None:
    """
    Ajoute une commande pour une table.
    Si la dernière commande enregistrée est pour la même table et qu'elle est encore occupée,
    elle est mise à jour. Sinon, une nouvelle entrée est ajoutée.

    :param table_id: Identifiant de la table.
    :param order: Contenu de la commande à enregistrer.
    """
    data = read_orders()
    if data and data[-1]["table"] == table_id and data[-1]["status"] == "occupied":
        data[-1]["order"] = order
    else:
        data.append({
            "table": table_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": "occupied",
            "order": order
        })
    write_orders(data)
    

def close_table(table_id: int) -> None:
    """
    Marque la dernière commande occupée d'une table comme libre.

    :param table_id: Identifiant de la table à libérer.
    """
    data = read_orders()
    for entry in reversed(data):
        if entry["table"] == table_id and entry["status"] == "occupied":
            entry["status"] = "free"
            break
    write_orders(data)

def get_last_order(table_id: int) -> dict | None:
    """
    Récupère la dernière commande active (occupée) pour une table.

    :param table_id: Identifiant de la table.
    :return: Le contenu de la commande si elle existe, sinon None.
    """
    data = read_orders()
    for entry in reversed(data):
        if entry["table"] == table_id and entry["status"] == "occupied":
            return entry["order"]
    return None
