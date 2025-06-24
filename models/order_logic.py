def calculer_total(order: dict) -> float:
    """
    Calcule le total d'une commande en fonction des quantités et des prix.

    :param order: Dictionnaire contenant les entrées, plats et desserts.
    :return: Total de la commande.
    """
    return sum(
        item["price"] * item["qty"]
        for key in ("entrees", "plats", "desserts")
        for item in order.get(key, [])
    )
