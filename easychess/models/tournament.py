import json
import logging

from easychess.models.player import Player
from easychess.models.round import Round


class Tournament:
    """
    Represents a chess tournament.

    Attributes:
        name (str): The name of the tournament.
        location (str): The location of the tournament.
        start_date (datetime): The start date and time of the tournament.
        end_date (datetime): The end date and time of the tournament.
        number_of_rounds (int): The total number of rounds in the tournament.
        current_round (int): The current round being played.
        list_rounds (list): A list of rounds in the tournament.
        players (list): A list of players participating in the tournament.
        description (str): A description of the tournament.
    """

    def __init__(
        self,
        name,
        location,
        description,
        start_date=None,
        end_date=None,
        number_of_rounds=None,
        current_round=1,
        list_rounds=[],
        players=[],
        status=None,
    ):
        """
        Initializes a new tournament with specified details.

        Args:
            name (str): The name of the tournament.
            location (str): The location where the tournament is held.
            description (str): A description of the tournament.
        """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.list_rounds = list_rounds
        self.players = players
        self.description = description
        self.status = status

    def __str__(self):
        """
        Returns a string representation of the tournament.

        Returns:
            str: A formatted string with tournament details.
        """
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
        """
        Creates a new Tournament instance from given tournament details.

        Args:
            new_tournament (tuple): A tuple containing the tournament's name, location, and description.

        Returns:
            Tournament: An instance of the Tournament class.
        """
        name, location, description = new_tournament
        return cls(name, location, description)

    @classmethod
    def read(cls, file_path):
        """
        Reads tournament data from a specified JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The tournament data as a dictionary, or an empty dictionary if the file is not found.
        """
        try:
            with open(file_path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

    @classmethod
    def save(cls, file_path, tournament_data):
        """
        Saves tournament data to a specified JSON file.

        Args:
            file_path (str): The path to the JSON file.
            tournament_data (dict): The tournament data to be saved.
        """
        try:
            existing_data = cls.read(file_path)
            tournament_name = tournament_data["name"]
            for key, existing_tournament in existing_data.items():
                if existing_tournament["name"] == tournament_name:
                    existing_data[key] = tournament_data
                    break
            else:
                tournament_key = f"tournament{len(existing_data) + 1}"
                existing_data[tournament_key] = tournament_data
            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file)
        except Exception as e:
            logging.error(f"An error occurred while saving data to {file_path}: {e}")

    def as_dict(self):
        """
        Converts the tournament instance into a dictionary.

        Returns:
            dict: A dictionary representation of the tournament instance.
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d/%m/%Y %H:%M") if self.start_date else None,
            "end_date": self.end_date.strftime("%d/%m/%Y %H:%M") if self.end_date else None,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": self.players,
            "list_rounds": [round_.as_dict() for round_ in self.list_rounds] if self.list_rounds else [],
            "description": self.description,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("La donnée doit être un dictionnaire")
        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            number_of_rounds=data["number_of_rounds"],
            current_round=data["current_round"],
            players=[Player.from_dict(player) for player in data["players"]],
            list_rounds=[Round.from_dict(round) for round in data["list_rounds"]],
            description=data["description"],
            status=data["status"],
        )
