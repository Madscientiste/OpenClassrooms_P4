from .cmd_player import CreatePlayer, DeletePlayer, FindPlayer

from .abc import BaseCommand

from app.models import Player, Tournament
from app.utilities.decorators import sanitize_params
from app.utilities.handler import CommandHandler
from app.views import PlayerView


@CommandHandler.register_command
class PlayerCommand(BaseCommand):
    name = "player"
    usage = "player <sub_command>"
    description = "Player related command"

    sub_commands = {}
    sub_commands["create"] = CreatePlayer
    sub_commands["delete"] = DeletePlayer
    sub_commands["findby"] = FindPlayer

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.cmd_context = cmd_context

        self.context = BaseCommand.context.copy()
        self.context["sub_commands"] = self.sub_commands
        self.context["player_view"] = PlayerView()
        self.context["player_model"] = Player

    @sanitize_params
    def execute(self, action, args):
        self.execute_sub(action, args=args)
