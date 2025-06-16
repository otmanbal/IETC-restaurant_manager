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
