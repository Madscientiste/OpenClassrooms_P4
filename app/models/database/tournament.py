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
        round_instances=[],
        state=other.State(),
    ):
        self.id: int = doc_id or id
        self.name: str = name
        self.location: str = location
        self.date: str = date
        self.rounds: int = rounds
        self.round_instances: list[other.Round] = round_instances
        self.players: list[dbModel.Player] = players
        self.time_control: str = time_control
        self.desc: str = desc
        self.state: other.State = state

    def generate_round(self) -> other.Round:
        """Generate a round"""
        assert len(self.players) % 2 == 0, "Players not equal"

        if len(self.round_instances) < 1:
            players = deepcopy(sorted(self.players, key=lambda player: int(player.rank), reverse=True))

            round = other.Round()

            length = len(players)
            middle_index = length // 2

            superieur = players[:middle_index]
            inferieur = players[middle_index:]

            for player1, player2 in zip(superieur, inferieur):
                player1: other.Player
                player2: other.Player

                player1.history.append(player2.id)
                player2.history.append(player1.id)
                
                round.add_match(other.Match(player1, player2))

            return round
        else:
            previous_round = self.round_instances[self.state.current_round - 1]
            previous_players = previous_round.get_players()
            players = sorted(previous_players, key=lambda player: int(player.rank), reverse=True)

            round = other.Round()

            locked_ids = []

            # sortby_id = lambda _interable: sorted(_interable, key=lambda x: x.id)

            # # Ensuring they are matching
            # self.players = sortby_id(self.players)
            # previous_players = sortby_id(previous_players)

            # #: Sorting the self.players based on the previous round's players's points
            # players = [
            #     x
            #     for x, _ in sorted(
            #         zip(self.players, previous_players),
            #         key=lambda player: (float(player[1].points), int(player[1].rank)),
            #         reverse=True,
            #     )
            # ]

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

                    round.add_match(other.Match(player, opponent))
                    break

            return round
