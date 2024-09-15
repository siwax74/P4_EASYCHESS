class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.score1 = 0
        self.player2 = player2
        self.score2 = 0

    @classmethod
    def create(
        cls,
        player1,
        player2,
    ):
        return cls(player1, player2)

    def __str__(self):
        """Représentation en chaîne de caractères de l'objet Match."""
        return f"{self.player1['first_name']} {self.player1['last_name']}, {self.score1} VS {self.player2['first_name']} {self.player2['last_name']}, {self.score2}"

    def as_dict(self):
        return {
            'player1': self.player1,
            'score1': self.score1,
            'player2': self.player2,
            'score2': self.score2,

        }
    
    def __repr__(self):
        return (f"Match(player1={self.player1!r}, score1={self.score1!r}, "
                f"player2={self.player2!r}, score2={self.score2!r})")