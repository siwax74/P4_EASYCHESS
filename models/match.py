class Match:
    def __init__(self, player1, score1, player2, score2):
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    @classmethod
    def create(cls, player1, score1, player2, score2):
        return cls(player1, score1, player2, score2)

    def __repr__(self):
        """Représentation en chaîne de caractères de l'objet Match."""
        return f"{self.player1['first_name']} {self.player1['last_name']}, {self.score1} VS {self.player2['first_name']} {self.player2['last_name']}, {self.score2}"
