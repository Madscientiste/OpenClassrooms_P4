# flake8: noqa

from copy import deepcopy
from tinydb import TinyDB

from .abc import BaseDB, STORAGE_PATH
from app.models import database as dbModel, other


class Tournament(BaseDB):
    database = TinyDB(STORAGE_PATH / "tournaments.json")
    resolvables = {"players": other.Player, "round_instances": other.Round, "state": other.State}

    def __init__(
        self,
        name=str(),
        location=str(),
        date=str(),
        rounds=4,
        players=[],
        time_control=str(),
        desc=str(),
        doc_id=int(),
        id=int(),
        round_instances=None,
        state=None,
    ):
        self.id: int = doc_id or id
        self.name: str = name
        self.location: str = location
        self.date: str = date
        self.rounds: int = rounds
        self.round_instances: list[other.Round] = round_instances or []
        self.players: list[dbModel.Player] = players
        self.time_control: str = time_control
        self.desc: str = desc
        self.state: other.State = state or other.State()

    def generate_round(self) -> other.Round:
        """Generate a round"""
        assert len(self.players) % 2 == 0, "No more room to generate a round"

        new_round = other.Round()

        if len(self.round_instances) < 1:
            players = deepcopy(sorted(self.players, key=lambda player: int(player.rank), reverse=True))

            length = len(players)
            middle_index = length // 2

            superieur = players[:middle_index]
            inferieur = players[middle_index:]

            for player1, player2 in zip(superieur, inferieur):
                player1: other.Player
                player2: other.Player

                player1.history.append(player2.id)
                player2.history.append(player1.id)

                new_round.add_match(other.Match(player1, player2))

            return new_round
        else:
            previous_round = self.round_instances[self.state.current_round - 1]
            previous_players = deepcopy(previous_round.get_players())
            players = sorted(previous_players, key=lambda player: int(player.rank), reverse=True)

            locked_ids = []

            for player in players:
                player: other.Player
                if player.id in locked_ids:
                    continue

                locked_ids.append(player.id)

                for opponent in players:
                    opponent: other.Player
                    if opponent.id in locked_ids or opponent.id in player.history:
                        continue

                    locked_ids.append(opponent.id)
                    player.history.append(opponent.id)
                    opponent.history.append(player.id)

                    player.points = 0
                    opponent.points = 0

                    new_round.add_match(other.Match(player, opponent))
                    break

            return new_round
