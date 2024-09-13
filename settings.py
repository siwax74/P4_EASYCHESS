from pathlib import Path

# Définir le répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent

PLAYERS_FILE = BASE_DIR / "datas" / "data_players.json"
TOURNAMENT_FILE = BASE_DIR / "datas" / "data_tournament.json"