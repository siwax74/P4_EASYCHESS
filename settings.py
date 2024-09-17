from pathlib import Path

# Définir le répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

PLAYERS_FILE = BASE_DIR / "easychess" / "datas" / "data_players.json"
TOURNAMENTS_FILE = BASE_DIR / "easychess" / "datas" / "data_tournament.json"
