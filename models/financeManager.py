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

def save_finance_entry(entry):
    """
    Permet de sauvegarder une nouvelle entrée financière en l’ajoutant
    aux données existantes dans le fichier JSON des finances.
    """
    data = load_finances()
    data.append(entry)
    with open(FINANCE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_financial_record(record_type, description, amount):
    """
    Permet d’ajouter un enregistrement financier avec la date du jour, puis de le sauvegarder dans le fichier JSON des finances.
    """
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": record_type,
        "description": description,
        "amount": amount
    }
    save_finance_entry(entry)
