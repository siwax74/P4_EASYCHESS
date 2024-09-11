from datetime import datetime
import json
import logging
import pprint
from typing import Dict, List
from models.player import Player
from models.round import Round


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

    @classmethod
    def create(cls, name, location, start_date, end_date, description):
        return cls(
            name,
            location,
            start_date,
            end_date,
            description,
        )

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
            existing_data[tournament_key] = tournament_data
            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)
        except Exception as e:
            logging.error(f"An error occurred while saving data to {file_path}: {e}")

    @staticmethod
    def add_player_auto(file_player, tournament_data):
        try:
            existing_player = Player.read(file_player)
            for player in existing_player:
                tournament_data["players"].append(player)
            return tournament_data
        except FileNotFoundError:
            raise Exception("Le fichier des joueurs est introuvable.")
        except json.JSONDecodeError:
            raise Exception("Erreur de décodage JSON dans le fichier des joueurs.")
        except Exception as e:
            raise Exception(f"Une erreur est survenue : {str(e)}")

    @staticmethod
    def add_player_manual(selected_players, players, tournament_data):
        try:
            selected_players = [int(i) - 1 for i in selected_players.split()]
            for idx in selected_players:
                if 0 <= idx < len(players):
                    player = players[idx]
                    tournament_data["players"].append(player)
                else:
                    raise IndexError("Le joueur à cet index n'existe pas.")
            return tournament_data
        except Exception as e:
            raise Exception(f"Une erreur est survenue : {str(e)}")

    def as_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "number_of_rounds": self.number_of_rounds,
            "players": self.players,
            "current_round": self.current_round,
            "list_rounds": self.list_rounds,
            "description": self.description,
        }
