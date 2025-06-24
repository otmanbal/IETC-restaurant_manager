from dataclasses import dataclass

@dataclass
class menu:
    """
    Classe de base représentant un élément du menu avec un nom et un prix.
    """
    name: str
    price: float

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de l'objet menu.

        :return: Chaîne formatée du type "Nom – Prix €"
        """
        return f"{self.name} – {self.price:.2f} €"

"""Représente une entrée du menu."""
class Entree(menu): pass
"""Représente un plat principal du menu."""
class Plat(menu): pass
"""Représente un dessert du menu."""
class Dessert(menu): pass

CARTE_ENTREES = [
    Entree("Accra de morue (beignets de poisson)", 6.00),
    Entree("Salade de papaye verte", 5.50),
    Entree("Briouates au fromage", 6.20),
    Entree("Zaalouk (caviar d’aubergine)", 5.80),
    Entree("Taboulé libanais", 6.00),
    Entree("Houmous traditionnel", 5.50),
]

CARTE_PLATS = [
    Plat("Poulet DG (Directeur Général)", 17.50),
    Plat("Ndolé crevettes & arachides", 18.00),
    Plat("Tajine d’agneau aux pruneaux", 18.50),
    Plat("Couscous royal", 17.90),
    Plat("Chiche taouk (brochettes de poulet)", 16.50),
    Plat("Kefta de boeuf grillée", 15.00),
]

CARTE_DESSERTS = [
    Dessert("Beignets banane", 4.20),
    Dessert("Puff‑puff & sirop", 4.00),
    Dessert("Chebakia au miel", 4.50),
    Dessert("Pastilla au lait", 4.80),
    Dessert("Baklava pistache", 4.20),
    Dessert("Mouhalabieh (flan au lait parfumé)", 4.00),
]
