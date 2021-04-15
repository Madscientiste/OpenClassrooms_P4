from .cmd_tournament import CreateTournament, DeleteTournament, StartTournament, ShowTournament
from .abc import BaseCommand

from app.models import Tournament, Player
from app.utilities.decorators import sanitize_params
from app.views import PlayerView, TournamentView
from app.utilities.handler import CommandHandler


@CommandHandler.register_command
class TournamentCommand(BaseCommand):
    name = "tournament"
    usage = "tournament <sub_command>"
    description = "tournament related command"

    sub_commands = {}
    sub_commands["create"] = CreateTournament
    sub_commands["delete"] = DeleteTournament
    sub_commands["start"] = StartTournament
    sub_commands["show"] = ShowTournament

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.cmd_context = cmd_context

        self.context = BaseCommand.context.copy()
        self.context["sub_commands"] = self.sub_commands

        self.context["tournament_view"] = TournamentView()
        self.context["player_view"] = PlayerView()
        self.context["tournament_model"] = Tournament
        self.context["player_model"] = Player

    @sanitize_params
    def execute(self, action, args):
        self.execute_sub(action, args=args)
