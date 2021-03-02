from app.models import Player, Tournament
from app.views import PlayerView


class BaseCommand:
    name = None
    usage = None
    description = None

    sub_commands = {}

    player_model = Player
    tournament_model = Tournament

    player_view = PlayerView()

    def __init__(self) -> None:
        pass

    def sanitize_action(self, args) -> None:
        pass

    def execute(self, args):
        pass

    def execute_sub(self, sub_cmd, *args, **kwargs):
        sub_cmd = self.sub_commands.get(sub_cmd)

        if not sub_cmd:
            return None

        sub_cmd(*args, **kwargs)
