import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

FILE = Path(__file__).parent.parent / "database" / "orders.json"
# Si orders.json existe on lit le fichier JSON et on retourne une liste de dictionnaires
