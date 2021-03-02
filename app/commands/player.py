from .cmd_player import create, update, delete, find

from .abc import BaseCommand


class PlayerCommand(BaseCommand):
    name = "player"
    usage = "player <sub_command>"
    description = "Player related command"

    sub_commands = {}
    sub_commands["create"] = create
    sub_commands["update"] = update
    sub_commands["delete"] = delete
    sub_commands["find"] = find

    def execute(self, args):
        action = args.pop(0) if len(args) else None

        if not action:
            return print("no action specified")

        # Prepare the context so it cas passe into its childrens
        context = {}
        context["player_model"] = self.player_model
        context["player_view"] = self.player_view

        self.execute_sub(action, context)
