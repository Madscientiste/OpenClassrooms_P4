from .base import BaseCommand
from app.controllers import Commands

from app.utilities import typings, errors


class Command(BaseCommand):
    name = "player"
    usage = "player <command>"
    description = "Player related command"

    def __init__(self) -> None:
        self.commands = Commands(package="app.commands.cmd_player", parent_command=self.name)

    def run(self, context: typings.Context, args: list):
        try:
            main_view = context["views"]["main"]

            sub_commands = self.commands.cache.values()
            main_view.render_available_commands(sub_commands)

            command_name = args.pop(0) if args else None
            self.commands.execute(command_name, args=args, context=context)

        except Exception as e:
            if not hasattr(e, "custom"):
                errors.GenericError(e)

            main_view.render_available_commands(sub_commands)