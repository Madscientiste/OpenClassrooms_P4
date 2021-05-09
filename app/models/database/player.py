from tinydb import TinyDB
from .abc import BaseDB, STORAGE_PATH


class Player(BaseDB):
    database = TinyDB(STORAGE_PATH / "players.json")
    resolvables = {}

    def __init__(
        self,
        first_name=str(),
        last_name=str(),
        birthday=str(),
        sexe=str(),
        rank=int(),
        doc_id=int(),
        id=int(),
    ):
        self.id = doc_id or id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.sexe = sexe
        self.rank = rank

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
