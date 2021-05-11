# flake8: noqa
from copy import deepcopy

from app.commands.base import BaseCommand
from app.models import database
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "commit"
    usage = "commit"
    description = "Commit the players's poitns into their global rank"

    def run(self, tournament: database.Tournament, *args, **kwargs):
        if tournament.state.commit:
            raise errors.GenericError("This tournament has been already commited")

        sortby_id = lambda _interable: sorted(_interable, key=lambda x: x.id)
        base_players = sortby_id(tournament.players)

        for round in tournament.round_instances:
            players = sortby_id(round.get_players())

            for base_player, new_player in zip(base_players, players):
                base_player.rank += new_player.points

        tournament.state.commit = True