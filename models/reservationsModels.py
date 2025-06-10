import json
from collections import defaultdict

class ReservationModel:
    @staticmethod
    def load_reservations(json_path):
        """Charge les réservations depuis un fichier JSON."""
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
