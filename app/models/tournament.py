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

        self.state = {"current_round": None, "rounds": {}}

    def save(self):
        """Save the current player into the database"""
        tournament = self.__dict__
        tournament_id = self.tournaments.insert(tournament)
        saved_tournament = self.tournaments.get(doc_id=tournament_id)

        return saved_tournament

    @classmethod
    def update_one(cls, tournament):
        pass

    @classmethod
    def find_all(cls):
        found_tournaments = cls.tournaments.all()
        return found_tournaments

    @classmethod
    def find_one(cls, id) -> list:
        """Find one tournament by ID
        returns tournament
        """
        found_tournament = cls.tournaments.get(doc_id=int(id))
        return found_tournament


## turn == 1 jour de tournois
## match == 1 entre 2 joueurs
## turn has many matches