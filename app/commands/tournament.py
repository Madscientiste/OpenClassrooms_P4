from .base import BaseCommand

from app.utilities import typings
from app.controllers import Commands


class Command(BaseCommand):
    name = "tournament"
    usage = "tournament <command>"
    description = "tournament related command"

    def __init__(self) -> None:
        self.commands = Commands(package="app.commands.cmd_tournament", parent_command=self.name)

    def run(self, context: typings.Context, args: list):
        self._run(context, args)
