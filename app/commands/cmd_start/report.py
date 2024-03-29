# flake8: noqa
from copy import deepcopy

from app.commands.base import BaseCommand
from app.models import database
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "report"
    usage = "report <sort_key> <order (accending or deccending)>"
    description = "Show the report of the current Tournament"

    def run(self, tournament: database.Tournament, context: typings.Context, args: list):
        tournament_view = context["views"]["tournament"]

        sort_by = self.pop_arg(args) or "points"
        order = self.pop_arg(args) or "ascending"

        if order not in ["ascending", "descending"]:
            errors.GenericError(f"Can't set the order to {order}, use ascending or descending.")

        sortby_id = lambda _interable: sorted(_interable, key=lambda x: x.id)
        base_players = deepcopy(sortby_id(tournament.players))

        for round in tournament.round_instances:
            players = sortby_id(round.get_players())

            for base_player, new_player in zip(base_players, players):
                base_player.points += new_player.points

        tournament_view.render_report(base_players, sort_by, order)
