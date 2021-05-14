from tinydb import TinyDB
from .abc import BaseDB, STORAGE_PATH


class Player(BaseDB):
    database = TinyDB(STORAGE_PATH / "players.json")
    resolvables = {}

    def __init__(
        self,
        first_name=None,
        last_name=None,
        birthday=None,
        sexe=None,
        rank=None,
        doc_id=None,
        id=None,
    ):
        self.id = doc_id or id or int()
        self.first_name = first_name or str()
        self.last_name = last_name or str()
        self.birthday = birthday or str()
        self.sexe = sexe or str()
        self.rank = rank or int()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
