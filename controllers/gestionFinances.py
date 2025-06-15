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


def ajouterEntree(id, date, type_paiement, total_facture):
    """
        Vérifie que le type_paiement est bien soit "virement" soit "cache". Sinon, déclenche une erreur.
        Charge les données existantes du fichier JSON.
        Crée un dictionnaire représentant une nouvelle entrée de paiement
        Ajoute cette nouvelle entrée à la liste existante avec append().
        Sauvegarde la nouvelle liste dans le fichier JSON.
        Affiche un message de confirmation dans la console.
    """
    if type_paiement not in ["virement", "cache"]:
        raise ValueError("Type de paiement invalide. Utiliser 'virement' ou 'cache'.")
    
    donnees = chargerDonnees()
    entree = {
        "id": id,
        "date": date,
        "type_paiement": type_paiement,
        "total_facture": total_facture
    }

    donnees.append(entree)
    sauvegarderDonnees(donnees)
    print("Entrée ajoutée avec succès.")
