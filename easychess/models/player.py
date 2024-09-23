from datetime import datetime
import json
from typing import Dict


class Player:
    def __init__(
        self,
        last_name: str,
        first_name: str,
        birthdate: str,
        national_id: str,
        score: float = 0,
    ) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = datetime.strptime(birthdate, "%d/%m/%Y")
        self.national_id = national_id
        self.score = score

    def __str__(self):
        return (
            f"Nom: {self.last_name}, Prénom: {self.first_name}, "
            f"Date de naissance: {self.birthdate.strftime('%d/%m/%Y')}, "
            f"National ID: {self.national_id}"
        )

    @classmethod
    def create(cls, player_info):
        first_name, last_name, birthdate, national_id = player_info
        return cls(first_name, last_name, birthdate, national_id)

    @classmethod
    def read(cls, file_path: str) -> Dict[str, Dict[str, str]]:
        try:
            with open(file_path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

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

    def update_score(self, points):
        self.score += points

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthdate=data["birthdate"],
            national_id=data["national_id"],
            score=data["score"],
        )

    def as_dict(self) -> Dict[str, str]:
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate.strftime("%d/%m/%Y"),
            "national_id": self.national_id if self.national_id else None,
            "score": self.score,
        }
