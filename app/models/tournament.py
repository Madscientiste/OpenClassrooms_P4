from app.database import TINY_DB_PATH

from tinydb import TinyDB, Query


class Tournament:
    def __init__(self, name, location, date, turns, players, time_control, description) -> None:
        self.name = name
        self.location = location
        self.date = date
        self.turns = turns
        self.players = players
        self.time_control = time_control
        self.description = description

    def save(self):
        tournaments = TinyDB(TINY_DB_PATH / "tournaments.json")
        inserted_tournament = tournaments.insert(self.__dict__)
        return inserted_tournament


## turn == 1 jour de tournois
## match == 1 entre 2 joueurs
## turn has many matches