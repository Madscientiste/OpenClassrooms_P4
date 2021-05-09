from app.commands.base import BaseCommand
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "findby"
    usage = "player findby <key> <value>"
    description = "Find a player by a key, omitting the key will return all the created players."

    def run(self, context: typings.Context, args: list):
        player_model = context["models"]["Player"]
        player_view = context["views"]["player"]

        key = self.pop_arg(args)
        value = self.pop_arg(args)

        if key and not value:
            raise errors.GenericError(f"Missing value for {key}")

        found_players = player_model.find_many(key, value)

        if not found_players:
            raise errors.GenericError("No players found")

        player_view.render_multiples(found_players, title="Found Players")
