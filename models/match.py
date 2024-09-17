class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.score1 = 0
        self.player2 = player2
        self.score2 = 0

    @classmethod
    def create(cls, player1, player2):
        return cls(player1, player2)

    def __str__(self):
        """Représentation en chaîne de caractères de l'objet Match."""
        return f"{self.player1['first_name']} {self.player1['last_name']} {self.score1:>2} - {self.score2:<2} {self.player2['first_name']} {self.player2['last_name']}"

    def set_score(self, score1, score2):
        """
        Set the scores for the match.
        :param score1: The score for player 1.
        :param score2: The score for player 2.
        """
        self.score1 = score1
        self.score2 = score2

    def as_tuple(self):
        return (
            [f"{self.player1['last_name']} {self.player1['first_name']}", self.score1],
            [f"{self.player2['last_name']} {self.player2['first_name']}", self.score2],
        )
