from app.database import TINY_DB_PATH

from tinydb import TinyDB, Query


class Tournament:
    tournaments = TinyDB(TINY_DB_PATH / "tournaments.json")

    def __init__(self, name, location, date, turns, players, time_control, description):
        self.name = name
        self.location = location
        self.date = date
        self.turns = turns
        self.players = players
        self.time_control = time_control
        self.description = description

    def save(self):
        """Save the current player into the database"""
        tournament = self.__dict__
        tournament_id = self.tournaments.insert(tournament)
        saved_tournament = self.tournaments.get(doc_id=tournament_id)

        return saved_tournament



## turn == 1 jour de tournois
## match == 1 entre 2 joueurs
## turn has many matches