from datetime import datetime


class Round:
    """
    Represents a round in a tournament.

    This class handles round data, including creation, adding matches,
    and converting to dictionary format.
    """

    def __init__(self, name, start_date_time, end_date_time):
        """
        Initialize a Round object.

        Args:
            name (str): The name of the round.
            start_date_time (datetime): The start date and time of the round.
            end_date_time (datetime): The end date and time of the round.
        """
        self.name = name
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.matches = []

    def add_match(self, match):
        """
        Add a match to the round.

        Args:
            match (Match): The match object to add to the round.
        """
        self.matches.append(match)

    @classmethod
    def create(cls, name):
        """
        Create a new Round object with the current datetime as the start time.

        Args:
            name (str): The name of the round.

        Returns:
            Round: A new Round object.
        """
        return cls(name, datetime.now(), end_date_time=None)

    def as_dict(self):
        """
        Convert the Round object to a dictionary.

        Returns:
            dict: A dictionary representation of the Round object.
        """
        return {
            "name": self.name,
            "start_date_time": self.start_date_time.isoformat(),
            "end_date_time": self.end_date_time.isoformat() if self.end_date_time else None,
            "matches": [match.as_tuple() for match in self.matches] if self.matches else [],
        }

    def __repr__(self):
        """
        Return a string representation of the Round object.

        Returns:
            str: A string representation of the Round object.
        """
        return (
            f"Round(name={self.name!r}, "
            f"start_date_time={self.start_date_time.isoformat()!r}, "
            f"end_date_time={self.end_date_time.isoformat() if self.end_date_time else None!r}, "
            f"matches=[{', '.join(repr(match) for match in self.matches)}])"
        )
