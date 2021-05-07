from .abc import BaseModel

from app.models import other


class Match(BaseModel):
    resolvables = {"player1": other.Player, "player2": other.Player}

    def __init__(self, player1: other.Player, player2: other.Player, winner=None) -> None:
        self.player1 = player1
        self.player2 = player2

        self.winner = winner  # Player 1 or Player 2 or TIE

    def get_players(self) -> list[other.Player]:
        """Get all the players from the match"""
        return [self.player1, self.player2]

    def settle_score(self, winner) -> None:
        """Set the winner of the match"""
        if winner in [self.player1, self.player2, "TIE"]:
            self.winner: other.Player = winner
