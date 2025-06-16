from controllers.gestionFinances import chargerDonnees
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas




def exportPdf(texte):
    """
        Crée un objet canvas (feuille blanche PDF).
        la variable y représente la position verticale de départ pour 
        écrire le texte (en haut de la page moins une marge).

        Découpe le texte ligne par ligne.
        Affiche chaque ligne à l'écran à la position (x=50, y).
        Si on atteint le bas de la page (y < 50), une nouvelle page est créée
    """
    c = canvas.Canvas("Rapport_financier.pdf", pagesize = A4)
    width, height = A4
    y = height - 50

    for ligne in texte.split("\n"):
        c.drawString(50, y, ligne)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print("\n Rapport PDF sauvegardé dans 'rapport_financier.pdf'")


def generateReport():
    """
        La fonction commence par charger les données à partir du fichier JSON contenant les transactions financières. 
        Ensuite, elle initialise trois variables : "total_global" pour cumuler le montant total de toutes les factures, 
        "total_par_jour" pour regrouper les montants par date, et "total_par_type" pour 
        regrouper les montants par type de paiement (virement ou cache). Grâce à une boucle "for", 
        elle parcourt chaque entrée pour mettre à jour ces totaux. Une fois les calculs effectués, 
        la fonction construit un texte structuré contenant le titre du rapport, le total global,
        le total par jour, et par type de paiement. Ce texte est affiché dans le terminal, 
        puis sauvegardé dans un fichier texte "rapport_financier.txt", et enfin converti en PDF via la fonction "exporter_pdf()".
        Cette fonction automatise donc toute la génération et l’exportation d’un rapport clair, lisible et archivable.
    """
    donnees = chargerDonnees() 

    total_global = 0
    total_par_jour = defaultdict(float)
    total_par_type = defaultdict(float)

    for entree in donnees:
        total_global += entree["total_facture"]
        total_par_jour[entree["date"]] += entree["total_facture"]
        total_par_type[entree["type_paiement"]] += entree["total_facture"]


    lignes = []
    lignes.append("===== RAPPORT FINANCIER =====")
    lignes.append(f"Total global : {total_global:.2f} €\n")

    lignes.append("Total par jour :")
    for date, total in total_par_jour.items():
        lignes.append(f"  {date} : {total:.2f} €")

    lignes.append("\nTotal par type de paiement :")
    for type_paiement, total in total_par_type.items():
        lignes.append(f"  {type_paiement} : {total:.2f} €")

    rapport_texte = "\n".join(lignes)
    print(rapport_texte)

    with open("rapport_financier.txt", "w", encoding="utf-8") as fichier:
        fichier.write(rapport_texte)
        print("\n Rapport sauvegardé dans 'rapport_financier.txt'")

    exportPdf(rapport_texte)

if __name__ == "__main__":
    generateReport()
