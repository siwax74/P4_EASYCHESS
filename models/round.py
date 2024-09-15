from datetime import datetime


class Round:
    def __init__(self, name, start_date_time, end_date_time):
        self.name = name
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)

    @classmethod
    def create(cls, name):
        return cls(name, datetime.now(), end_date_time=None)

    def as_dict(self):
        return {
            "name": self.name,
            "start_date_time": self.start_date_time.isoformat(),
            "end_date_time": self.end_date_time.isoformat() if self.end_date_time else None,
            "matches": [match.as_dict() for match in self.matches]
        }

    def __repr__(self):
        return (f"Round(name={self.name!r}, "
                f"start_date_time={self.start_date_time.isoformat()!r}, "
                f"end_date_time={self.end_date_time.isoformat() if self.end_date_time else None!r}, "
                f"matches=[{', '.join(repr(match) for match in self.matches)}])")