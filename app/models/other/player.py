from .abc import BaseModel


class Player(BaseModel):
    resolvables = {}

    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        birthday: str = None,
        points: float = 0,
        history: list = [],
        sexe: str = None,
        rank: int = None,
        id: int = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.sexe = sexe
        self.rank = rank
        self.points = points
        self.history = history
