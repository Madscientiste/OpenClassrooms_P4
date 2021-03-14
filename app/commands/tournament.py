from .cmd_tournament import create, update, delete
from .abc import BaseCommand

from app.models import Tournament, Player
from app.decorators import sanitize_params
from app.views import PlayerView, TournamentView


class TournamentCommand(BaseCommand):
    name = "tournament"
    usage = "tournament <sub_command>"
    description = "tournament related command"

    sub_commands = {}
    sub_commands["create"] = create
    sub_commands["update"] = update
    sub_commands["delete"] = delete

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.cmd_context = cmd_context

        self.context = BaseCommand.context.copy()
        self.context["tournament_view"] = TournamentView()
        self.context["player_view"] = PlayerView()

        self.context["tournament_model"] = Tournament
        self.context["player_model"] = Player

    @sanitize_params
    def execute(self, action, args):
        self.execute_sub(action, context=self.context, args=args)
