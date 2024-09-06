from typing import Dict


class Match:
    def __init__(
        self, player1: str, score1: float, player2: str, score2: float
    ) -> None:
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def to_dict(self) -> Dict[str, any]:
        return {
            "player1": self.player1,
            "score1": self.score1,
            "player2": self.player2,
            "score2": self.score2,
        }
