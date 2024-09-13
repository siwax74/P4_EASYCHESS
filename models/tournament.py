from datetime import datetime
import json
import logging


class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        description,
    ):
        self.name = name
        self.location = location
        self.start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M")
        self.end_date = datetime.strptime(end_date, "%d/%m/%Y") if end_date else None
        self.number_of_rounds = 4
        self.current_round = 1
        self.list_rounds = []
        self.players = []
        self.description = description

    def __str__(self):
        return (
            f"{self.name} - {self.location} - {self.start_date} à {self.end_date}\n"
            f"Description: {self.description}\n"
            f"Number of rounds: {self.number_of_rounds}\n"
            f"Current round: {self.current_round}\n"
            f"List of rounds: {self.list_rounds}\n"
            f"Players: {[str(player) for player in self.players]}"
        )

    @classmethod
    def create(cls, player_info):
        name, location, start_date, end_date, description = player_info
        return cls(name, location, start_date, end_date, description)

    @classmethod
    def read(cls, file_path):
        try:
            with open(file_path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

    @classmethod
    def save(cls, file_path, tournament_data):
        try:
            existing_data = cls.read(file_path)
            tournament_key = f"tournament{len(existing_data) + 1}"
            tournament_data["upcoming"] = True
            tournament_data["in_progress"] = False
            existing_data[tournament_key] = tournament_data
            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)
        except Exception as e:
            logging.error(f"An error occurred while saving data to {file_path}: {e}")

    @classmethod
    def start(cls, tournament_info):
        players = tournament_info.get("players", [])
        print("Joueurs :", players)

    @staticmethod
    def add_players_auto(players, new_tournament):
        new_tournament.players.extend(players)
        return new_tournament()

    @staticmethod
    def add_players_manually(selected_players, players, new_tournament):
        try:
            selected_players = [int(i) - 1 for i in selected_players.split()]
            for idx in selected_players:
                if 0 <= idx < len(players):
                    player = players[idx]
                    new_tournament.players.append(player)
                else:
                    raise IndexError("Le joueur à cet index n'existe pas.")
            return new_tournament
        except Exception as e:
            raise Exception(f"Une erreur est survenue : {str(e)}")
        
    @staticmethod
    def generate_pairs(self):
        pairs = []
        for i in range(0, len(self.players) - 1, 2):
            pairs.append((self.players[i], self.players[i + 1]))
        return pairs
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            number_of_rounds=data["number_of_rounds"],
            current_round=data["current_round"],
            players=data["players"],
            list_rounds=data["list_rounds"],
            description=data["description"],
            upcoming=data["upcoming"],
            in_progress=data["in_progress"],
        )

    def as_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d/%m/%Y %H:%M"),
            "end_date": self.end_date.strftime("%d/%m/%Y") if self.end_date else None,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": self.players,
            "list_rounds": self.list_rounds,
            "description": self.description,
        }
