from app.commands.base import BaseCommand
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "findby"
    usage = "tournament findby <key> <value>"
    description = "Find a tournament by a key, omitting the key will return all the created tournaments."

    def run(self, context: typings.Context, args: list):
        tournament_model = context["models"]["Tournament"]
        tournament_view = context["views"]["tournament"]

        key = self.pop_arg(args)
        value = self.pop_arg(args)

        if key and not value:
            raise errors.GenericError(f"Missing value for {key}")

        if key and key not in vars(tournament_model()):
            raise errors.GenericError(f"The key <{key}> doesn't exist in tournament")

        found_tournaments = tournament_model.find_many(key, value)

        if not found_tournaments:
            raise errors.GenericError("No tournaments found")

        tournament_view.render_multiples(found_tournaments, title="Found tournaments")
