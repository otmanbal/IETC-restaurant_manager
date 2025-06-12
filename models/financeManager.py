import json
from datetime import datetime

FINANCE_FILE = "data/finances.json"

def load_finances():
    """
    Charge les données financières depuis le fichier JSON spécifié et retourne
    une liste de transactions si le fichier existe, sinon une liste vide.
    """
    try:
        with open(FINANCE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
