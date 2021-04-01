import re

from tinydb import TinyDB, Query

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

    @classmethod
    def delete_one(cls, id):
        """Delete a player by ID
        returns the deleted player
        """
        deleted = cls.players.remove(doc_id=[id])
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
            search_type = player[key] == value

            if key == "last_name" or key == "first_name":
                search_type = player[key].matches(value, re.IGNORECASE)
            
            elif key == "rank":
                search_type = player[key] == int(value)

            found_players = cls.players.search(search_type)

        else:
            found_players = cls.players.all()

        return found_players
