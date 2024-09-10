from datetime import datetime
from typing import Dict, List
from models.player import Player
from models.round import Round


class Tournament:
    def __init__(self, name, location, start_date, end_date, number_of_rounds, description, players):
        self.name = name
        self.location = location
        self.start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M")
        self.end_date = (
            datetime.strptime(end_date, "%d/%m/%Y") if end_date else None
        )
        self.number_of_rounds = number_of_rounds
        self.players = players
        self.current_round = 1
        self.rounds = []
        self.description = description

    def as_dict(self):
        """Convertit l'objet Tournament en dictionnaire pour la persistance JSON."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d/%m/%Y %H:%M"),
            "end_date": (
                self.end_date.strftime("%d/%m/%Y") if self.end_date else None
            ),
            "number_of_rounds": self.number_of_rounds,
            "players": self.players,
            "current_round": self.current_round,
            "rounds": self.rounds,
            "description": self.description,
        }

