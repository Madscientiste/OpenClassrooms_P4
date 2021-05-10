# flake8: noqa

from datetime import datetime

from .abc import BaseModel
from .match import Match

today = lambda: datetime.today().strftime("%d/%m/%Y %H:%M:%S")


class Round(BaseModel):
    resolvables = {"matches": Match}

    def __init__(self, matches: list[Match] = None, start_date: str = None, end_date: str = None) -> None:
        self.matches = matches or []

        self.start_date = start_date or today()  # 01/01/2001 15:00:00
        self.end_date = end_date

    def get_players(self):
        return [player for match in self.matches for player in match.get_players()]

    def end_round(self):
        self.end_date = today()

    def get_match(self, match_index: int) -> Match:
        """Get a match using its index"""
        return self.matches[match_index]

    def add_match(self, match):
        """Add a match to the round"""
        self.matches.append(match)
        return self
