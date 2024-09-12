from datetime import datetime


class Round:
    def __init__(self, name, start_date=None, end_date=None):
        self.name = name
        self.matches = []
        self.start_date = start_date or datetime.datetime.now()
        self.end_date = end_date

    def add_match(self, match):
        self.matches.append(match)

    def __repr__(self):
        return f"Round({self.name}, {self.start_date}, {self.end_date}, {self.matches})"
