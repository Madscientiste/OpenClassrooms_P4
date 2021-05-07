from app.models.database import player
from functools import reduce

from app.commands.base import BaseCommand
from app.utilities import typings, errors
from app.models import other, database


class Command(BaseCommand):
    name = "test"
    usage = "test"
    description = "Ayaya"
    is_hidden = True

    def run(self, context: typings.Context, tournament: database.Tournament, args: list, state: database.State):
        sortby_id = lambda _interable: sorted(_interable, key=lambda x: x.id)
        base_players = sortby_id(tournament.players)

        for round in tournament.round_instances:
            players = sortby_id(round.get_players())

            for base_player, new_player in zip(base_players, players):
                base_player.rank += new_player.points

