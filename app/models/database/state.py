from tinydb import TinyDB

from .abc import BaseDB, STORAGE_PATH


class State(BaseDB):
    database = TinyDB(STORAGE_PATH / "state.json")
    resolvables = {}

    def __init__(
        self,
        doc_id: int = None,
        id: int = None,
        tournament_id: int = None,
        current_round: int = 0,
        is_ongoing: bool = True,
    ):
        self.id = tournament_id or doc_id or id
        self.current_round = current_round
        self.is_ongoing = is_ongoing
