import random
import time

from .abc import BaseCommand

from app.models import Tournament, Player
from app.utilities.decorators import sanitize_params
from app.views import PlayerView, TournamentView
from app.utilities.handler import CommandHandler


@CommandHandler.register_command
class TestCommand(BaseCommand):
    name = "test"
    usage = "test"
    description = "Test Command"
    is_hidden = True

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.context = BaseCommand.context.copy()
        self.context["tournament_view"] = TournamentView()
        self.context["player_view"] = PlayerView()

        self.context["tournament_model"] = Tournament
        self.context["player_model"] = Player

    def execute(self, args):
        player_model = self.context["player_model"]
        players = player_model.find_many(None, None)

        tournament_rounds = 4

        # select 8 players and sort
        players = players[0:8]
        players = sorted(players, key=lambda player: int(player["rank"]), reverse=True)

        # split the array in half
        length = len(players)
        middle_index = length // 2

        superieur = players[:middle_index]
        inferieur = players[middle_index:]

        print("=".center(30, "="))
        print("Round 1".center(30, "="))
        print("=".center(30, "="))

        paired = []
        for p1, p2 in zip(superieur, inferieur):
            player1 = p1
            player2 = p2

            rand_score1 = random.randint(0, 1)
            rand_score2 = random.randint(0, 1)

            selective_score1 = rand_score1 / 2 if rand_score1 == 1 and rand_score2 == 1 else rand_score1
            selective_score2 = rand_score2 / 2 if rand_score1 == 1 and rand_score2 == 1 else rand_score2

            # populate the properties
            player1["points"] = selective_score1
            player2["points"] = selective_score2

            player1["history"] = [player2.doc_id]
            player2["history"] = [player1.doc_id]

            print(f' {player1["first_name"]} < VS > {player2["first_name"]} '.center(30, "-"))
            print(f' {player1["points"]} <--> { player2["points"]} '.center(30, "-"))
            print("=".center(30, "="))

            paired.extend([player1, player2])

        #
        for i in range(4):
            players = sorted(paired, key=lambda player: player["points"], reverse=True)

            # print("=".center(30, "="))
            # print([player["first_name"] for player in players])
            # print("=".center(30, "="))

            print("=".center(30, "="))
            print(f"Round {i + 2}".center(30, "="))
            print("=".center(30, "="))

            # Keeping track of the available players, locked mean they are already paired
            locked = []
            pairing = []

            for p1_index, current_player in enumerate(players):
                if p1_index not in locked:
                    print(f"-".center(30, "-"))
                    locked.append(p1_index)

                    for p2_index, next_player in enumerate(players):
                        if p2_index in locked or next_player.doc_id in current_player["history"]:
                            continue

                        locked.append(p2_index)
                        pairing.append([current_player, next_player])

                        rand_score1 = random.randint(0, 1)
                        rand_score2 = random.randint(0, 1)

                        selective_score1 = rand_score1 / 2 if rand_score1 == 1 and rand_score2 == 1 else rand_score1
                        selective_score2 = rand_score2 / 2 if rand_score1 == 1 and rand_score2 == 1 else rand_score2

                        # populate the properties
                        current_player["points"] = selective_score1
                        next_player["points"] = selective_score2

                        current_player["history"].append(current_player.doc_id)
                        next_player["history"].append(next_player.doc_id)

                        print(f' {current_player["first_name"]} < VS > {next_player["first_name"]} '.center(30, "-"))
                        print(f' {current_player["points"]} <--> {next_player["points"]} '.center(30, "-"))

                        break

                    print(f"-".center(30, "-"))
