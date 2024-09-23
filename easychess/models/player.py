from datetime import datetime
import json


class Player:
    """
    Represents a player with personal information and a score.

    This class handles player data, including creation, reading from and saving to JSON files,
    and score updates.
    """

    def __init__(self, last_name, first_name, birthdate, national_id, score=0):
        """
        Initialize a Player object.

        Args:
            last_name (str): The player's last name.
            first_name (str): The player's first name.
            birthdate (str): The player's birthdate in 'dd/mm/yyyy' format.
            national_id (str): The player's national ID.
            score (float, optional): The player's score. Defaults to 0.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = datetime.strptime(birthdate, "%d/%m/%Y")
        self.national_id = national_id
        self.score = score

    def __str__(self):
        """
        Return a string representation of the Player.

        Returns:
            str: A formatted string containing the player's information.
        """
        return (
            f"Nom: {self.last_name}\n"
            f"Prénom: {self.first_name}\n"
            f"Date de naissance: {self.birthdate.strftime('%d/%m/%Y')}\n"
            f"National ID: {self.national_id}"
        )

    @classmethod
    def create(cls, player_info):
        """
        Create a Player object from a tuple of player information.

        Args:
            player_info (tuple): A tuple containing first_name, last_name, birthdate, and national_id.

        Returns:
            Player: A new Player object.
        """
        first_name, last_name, birthdate, national_id = player_info
        return cls(first_name, last_name, birthdate, national_id)

    @classmethod
    def read(cls, file_path):
        """
        Read player data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: A dictionary of player data, or an empty dict if the file is not found.
        """
        try:
            with open(file_path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

    @classmethod
    def save(cls, file_path, player_data):
        """
        Save player data to a JSON file.

        Args:
            file_path (str): The path to the JSON file.
            player_data (dict): The player data to save.
        """
        try:
            existing_data = cls.read(file_path)
            if not existing_data:
                existing_data = []
            existing_data.append(player_data)
            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving data to {file_path}: {e}")

    def update_score(self, points):
        """
        Update the player's score.

        Args:
            points (float): The points to add to the player's score.
        """
        self.score += points

    @classmethod
    def from_dict(cls, data):
        """
        Create a Player object from a dictionary.

        Args:
            data (dict): A dictionary containing player information.

        Returns:
            Player: A new Player object.
        """
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthdate=data["birthdate"],
            national_id=data["national_id"],
            score=data["score"],
        )

    def as_dict(self):
        """
        Convert the Player object to a dictionary.

        Returns:
            dict: A dictionary representation of the Player object.
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate.strftime("%d/%m/%Y"),
            "national_id": self.national_id if self.national_id else None,
            "score": self.score,
        }
