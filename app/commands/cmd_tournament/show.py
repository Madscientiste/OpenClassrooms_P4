from app.commands.base import BaseCommand
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "show"
    usage = "tournament show"
    description = "Show all the tournaments"

    def run(self, context: typings.Context, args: list):
        tournament_model = context["models"]["Tournament"]
        tournament_view = context["views"]["tournament"]

        all_tournaments = tournament_model.find_many()

        if not all_tournaments:
            raise errors.GenericError("Nothing to show")

        tournament_view.render_multiples(all_tournaments)