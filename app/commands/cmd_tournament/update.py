from app.commands.base import BaseCommand
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "update"
    usage = "tournament update <tournament_id> <key> <value>"
    description = "Update a tournament's info"

    def run(self, context: typings.Context, args: list):
        tournament_model = context["models"]["Tournament"]
        tournament_view = context["views"]["tournament"]

        tournament_id = self.pop_arg(args)
        key = self.pop_arg(args)
        value = self.pop_arg(args)

        if not tournament_id:
            raise errors.GenericError("Tournament id is required")

        blacklist = ["doc_id", "id", "round_instances", "players"]

        if key in blacklist:
            raise errors.GenericError(f"Can't edit {key}")

        if not value:
            raise errors.GenericError("Input not valid")

        tournament = tournament_model.find_one(tournament_id)

        sanitize_type = type(getattr(tournament, key))

        setattr(tournament, key, sanitize_type(value))
        tournament = tournament.save()

        tournament_view.render_single(tournament, title="Updated Tournament")
