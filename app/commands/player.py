from .base import BaseCommand
from app.controllers import Commands

from app.utilities import typings


class Command(BaseCommand):
    name = "player"
    usage = "player <command>"
    description = "Player related command"

    def __init__(self) -> None:
        self.commands = Commands(package="app.commands.cmd_player", parent_command=self.name)

    def run(self, context: typings.Context, args: list):
        self._run(context, args)
