from datetime import datetime
from typing import Dict


class Player:
    def __init__(
        self, last_name: str, first_name: str, birthdate: str, national_id: str
    ) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = datetime.strptime(birthdate, "%d/%m/%Y")
        self.national_id = national_id

    def as_dict(self) -> Dict[str, str]:
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate.strftime("%d/%m/%Y"),
            "national_id": self.national_id,
        }
