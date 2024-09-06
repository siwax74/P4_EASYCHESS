from typing import List, Dict
from models.match import Match
from datetime import datetime


class Round:
    def __init__(self, name: str) -> None:
        self.name = name
        self.matches: List[Match] = []
        self.start_time = datetime.now()
        self.end_time = None

    def as_dict(self) -> Dict[str, any]:
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }
