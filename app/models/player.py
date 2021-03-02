import re

from tinydb import TinyDB, Query, where

from app.database import TINY_DB_PATH


class Player:
    players = TinyDB(TINY_DB_PATH / "players.json")

    def __init__(self, first_name, last_name, birthday, sexe, rank):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.sexe = sexe
        self.rank = rank

    def save(self):
        """Save the current player into the database"""
        player = self.__dict__
        player_id = self.players.insert(player)
        saved_player = self.players.get(doc_id=player_id)

        return saved_player

    def delete_one(self, id):
        """Delete a player by ID
        returns the deleted player
        """
        deleted = self.players.remove(where("doc_id") == int(id))
        return deleted

    @classmethod
    def find_one(cls, id) -> list:
        """Find one Player by ID
        returns player
        """

        found_player = cls.players.get(doc_id=id)
        return found_player

    @classmethod
    def find_many(cls, key, value) -> list:
        """Find many players using a value in a field

        returns list of players
        """

        player = Query()
        found_players = None

        if key:
            if key == "first_name":
                found_players = cls.players.search(player[key].matches(value, re.IGNORECASE))
            elif key == "rank":
                found_players = cls.players.search(player[key] == int(value))
            else:
                found_players = cls.players.search(player[key] == value)
        else:
            found_players = cls.players.all()

        return found_players
