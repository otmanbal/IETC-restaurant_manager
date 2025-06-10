import json
from collections import defaultdict

class ReservationModel:
    @staticmethod
    def load_reservations(json_path):
        """Charge les réservations depuis un fichier JSON."""
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)


    @staticmethod
    def compute_daily_totals(reservations):
        """Calcule le total payé pour chaque jour."""
        daily_totals = defaultdict(float)
        for r in reservations:
            daily_totals[r["date"]] += r["price"]

        # Génère une liste formatée pour le tableau
        return [
            {"id": i + 1, "date": date, "total": total}
            for i, (date, total) in enumerate(sorted(daily_totals.items()))
        ]
