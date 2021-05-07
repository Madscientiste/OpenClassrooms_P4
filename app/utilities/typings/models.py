from typing import TypedDict

from app.models import database, other


class Models(TypedDict):
    Tournament: database.Tournament
    Player: database.Player
    Round: other.Round
    Match: other.Match
