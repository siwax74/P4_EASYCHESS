class Match:
    """
    Represents a match between two players.

    Attributes:
        player1 (dict): Dictionary containing information about the first player.
        score1 (int): Score of the first player.
        player2 (dict): Dictionary containing information about the second player.
        score2 (int): Score of the second player.
    """

    def __init__(self, player1, player2, score1=0, score2=0):
        """
        Initializes a new match.

        Args:
            player1 (dict): Dictionary containing information about the first player.
            player2 (dict): Dictionary containing information about the second player.
        """
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    @classmethod
    def create(cls, player1, player2):
        """
        Creates a new instance of Match.

        Args:
            player1 (dict): Dictionary containing information about the first player.
            player2 (dict): Dictionary containing information about the second player.

        Returns:
            Match: A new instance of the Match class.
        """
        return cls(player1, player2)

    def __str__(self):
        """
        Returns a string representation of the Match object.

        Returns:
            str: A formatted string representing the match with player names and scores.
        """
        return (
            f"{self.player1['first_name']} {self.player1['last_name']}\n"
            f"Score: {self.score1:>2} - {self.score2:<2}\n"
            f"{self.player2['first_name']} {self.player2['last_name']}"
        )

    def set_score(self, score1, score2):
        """
        Sets the scores for the match.

        Args:
            score1 (int): The score for player 1.
            score2 (int): The score for player 2.
        """
        self.score1 = score1
        self.score2 = score2

    def as_tuple(self):
        """
        Returns a tuple representation of the match.

        Returns:
            tuple: A tuple containing two lists, each with a player's full name and score.
        """
        return (
            [f"{self.player1['last_name']} {self.player1['first_name']}", self.score1],
            [f"{self.player2['last_name']} {self.player2['first_name']}", self.score2],
        )

    @classmethod
    def from_tuple(cls, match_tuple):
        player1_name, score1 = match_tuple[0]
        player2_name, score2 = match_tuple[1]
        player1_last_name, player1_first_name = player1_name.split()
        player2_last_name, player2_first_name = player2_name.split()
        player1 = {"last_name": player1_last_name, "first_name": player1_first_name}
        player2 = {"last_name": player2_last_name, "first_name": player2_first_name}
        return cls(player1, player2, score1, score2)
