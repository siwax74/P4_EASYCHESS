import json
import logging


class Tournament:
    def __init__(
        self,
        name,
        location,
        description,
    ):
        self.name = name
        self.location = location
        self.start_date = None
        self.end_date = None
        self.number_of_rounds = None
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
            f"Players: {self.players}"
        )

    @classmethod
    def create(cls, new_tournament):
        name, location, description = new_tournament
        return cls(name, location, description)

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
                json.dump(existing_data, json_file)
        except Exception as e:
            logging.error(f"An error occurred while saving data to {file_path}: {e}")

    def as_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d/%m/%Y %H:%M"),
            "end_date": self.end_date.strftime("%d/%m/%Y %H:%M"),
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": self.players,
            "list_rounds": [round_.as_dict() for round_ in self.list_rounds] if self.list_rounds else [],
            "description": self.description,
        }
