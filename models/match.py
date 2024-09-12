from typing import Dict


class Match:
    def __init__(self, player1, score1, player2, score2):
        self.players = [player1, player2]
        self.scores = [score1, score2]

    def __repr__(self):
        return f"Match({self.players[0]}, {self.scores[0]}, {self.players[1]}, {self.scores[1]})"
