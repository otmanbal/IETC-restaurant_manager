import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

FILE = Path(__file__).parent.parent / "database" / "orders.json"


# Si orders.json existe on lit le fichier JSON et on retourne une liste de dictionnaires
def read_orders() -> List[Dict[str, Any]]: #annotation de type de retour. Elle indique que la fonction retourne : une liste (List) de dictionnaires (Dict) chaque clé string et chaque valeur n'importe quel type
    if FILE.exists():
        with FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def write_orders(data: List[Dict[str, Any]]) -> None:
    with FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Si la dernière entrée du fichier est pour la même table et qu'elle est encore occupée, on met à jour la commande.
# Sinon, on crée une nouvelle entrée avec : le numéro de table, la date/heure actuelle, le statut "occupied" et le contenu de la commande
def add_order(table_id: int, order: Dict[str, Any]) -> None:
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
    data = read_orders()
    for entry in reversed(data):
        if entry["table"] == table_id and entry["status"] == "occupied":
            entry["status"] = "free"
            break
    write_orders(data)
