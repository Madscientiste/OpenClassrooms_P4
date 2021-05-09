from .abc import BaseModel


class State(BaseModel):
    resolvables = {}

    def __init__(
        self,
        current_round: int = 0,
        is_ongoing: bool = True,
    ):
        self.current_round = current_round
        self.is_ongoing = is_ongoing
