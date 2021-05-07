from app.commands.base import BaseCommand
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "update"
    usage = "player update <player_id> <key> <value>"
    description = "Find a player by a key"

    def run(self, context: typings.Context, args: list):
        player_model = context["models"]["Player"]
        player_view = context["views"]["player"]

        player_id = self.pop_arg(args)
        key = self.pop_arg(args)
        value = self.pop_arg(args)

        if not player_id:
            raise errors.GenericError(f"Player id is required")

        blacklist = ["doc_id", "id"]

        if key in blacklist:
            raise errors.GenericError(f"Can't edit {key}")

        if not value:
            raise errors.GenericError("Missing value")

        player = player_model.find_one(player_id)
        setattr(player, key, value)
        player = player.save()


        player_view.render_single(player, title="Updated Players")