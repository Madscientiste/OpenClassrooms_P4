# flake8: noqa

from app.commands.base import BaseCommand
from app.utilities import typings


class Command(BaseCommand):
    name = "create"
    usage = "tournament create"
    description = "Create a new tournament"

    def run(self, context: typings.Context, args: list):
        tournament_model = context["models"]["Tournament"]
        tournament_view = context["views"]["tournament"]

        # result = player_model.inquire()
        # new_player = player_model(**result)

        # print(new_player)
