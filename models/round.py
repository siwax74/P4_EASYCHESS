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
    def create(cls):
        return cls("Round 1", datetime.now(), None)

    def __repr__(self):
        return f"{self.name} (début : {self.start_date_time}, fin : {self.end_date_time})\nMatches:\n{', '.join(str(match) for match in self.matches)}"
    
    def as_dict(self):
        return {
            'name': self.name,
            'start_date_time': self.start_date_time.isoformat(),
            'end_date_time': self.end_date_time.isoformat() if self.end_date_time else None,
            'matches': self.matches
        }