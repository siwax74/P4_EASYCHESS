from datetime import datetime
import json
from typing import Dict


class Player:
    def __init__(
        self, last_name: str, first_name: str, birthdate: str, national_id: str
    ) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = datetime.strptime(birthdate, "%d/%m/%Y")
        self.national_id = national_id

    def __repr__(self) -> str:
        return f"Player(last_name={self.last_name}, first_name={self.first_name}, birthdate={self.birthdate.strftime('%d/%m/%Y')}, national_id={self.national_id})"

    @classmethod
    def create(
        cls, last_name: str, first_name: str, birthdate: str, national_id: str
    ) -> "Player":
        return cls(last_name, first_name, birthdate, national_id)

    @classmethod
    def read(cls, file_path: str) -> Dict[str, Dict[str, str]]:
        try:
            with open(file_path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

    @classmethod
    def update(
        cls, file_path: str, player_id: str, updated_data: Dict[str, str]
    ) -> None:
        try:
            data = cls.read(file_path)
            if player_id in data:
                data[player_id].update(updated_data)
                with open(file_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)
            else:
                print(f"Player ID {player_id} not found.")
        except Exception as e:
            print(f"An error occurred while updating data: {e}")

    @classmethod
    def delete(cls, file_path: str, player_id: str) -> None:
        try:
            data = cls.read(file_path)
            if player_id in data:
                del data[player_id]
                with open(file_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)
            else:
                print(f"Player ID {player_id} not found.")
        except Exception as e:
            print(f"An error occurred while deleting data: {e}")

    @classmethod
    def save(cls, file_path, player_data):
        try:
            existing_data = cls.read(file_path)
            if not existing_data:
                existing_data = []
            existing_data.append(player_data)
            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving data to {file_path}: {e}")

    def as_dict(self) -> Dict[str, str]:
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate.strftime("%d/%m/%Y"),
            "national_id": self.national_id,
        }
