import json
from datetime import datetime

FICHIER_JSON = 'database/finances.json'

def chargerDonnees():
    """ 
        Ouvre le fichier finances.json en lecture.
        Lit le contenu JSON et le convertit en liste Python avec json.load.
        Si le fichier n'existe pas encore (ex: première utilisation), retourne une liste vide.
    """
    try:
        with open(FICHIER_JSON, 'r', encoding='utf-8') as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []


def sauvegarderDonnees(donnees):
    """
        Ouvre le fichier en écriture.
        Ecrit les données passées en argument dans le fichier JSON, 
        avec indentation pour faciliter la lecture
    """
    with open(FICHIER_JSON, 'w', encoding='utf-8') as fichier:
        json.dump(donnees, fichier, indent = 4, ensure_ascii = False)
