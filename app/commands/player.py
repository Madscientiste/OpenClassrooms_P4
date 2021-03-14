from .cmd_player import create, update, delete, findby

from app.models import Player, Tournament
from app.decorators import sanitize_params
from app.views import PlayerView

from .abc import BaseCommand


class PlayerCommand(BaseCommand):
    name = "player"
    usage = "player <sub_command>"
    description = "Player related command"

    sub_commands = {}
    sub_commands["create"] = create
    sub_commands["update"] = update
    sub_commands["delete"] = delete
    sub_commands["findby"] = findby

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.cmd_context = cmd_context

        self.context = BaseCommand.context.copy()
        self.context["player_view"] = PlayerView()
        self.context["player_model"] = Player

    @sanitize_params
    def execute(self, action, args):
        self.execute_sub(action, context=self.context, args=args)
