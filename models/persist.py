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
        
