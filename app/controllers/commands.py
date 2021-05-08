from app.commands.base import BaseCommand
from app.utilities import errors

from .base import baseController


class Commands(baseController):
    def __init__(self, parent_command: str = None, *args, **kwargs) -> None:
        self.cache: dict[str, BaseCommand]
        self.parent_command = parent_command
        super().__init__(search_class="Command", *args, **kwargs)

    def execute(self, command_name: str, *args, **kwargs):

        if not command_name and not self.parent_command:
            raise errors.GenericError("Missing Command")

        if not command_name and self.parent_command:
            raise errors.AvailableCommands(commands=self.cache.values())

        command = self.cache.get(command_name)

        if not command:
            raise errors.CommandNotFound(command_name, parent_command=self.parent_command, commands=self.cache.values())

        if command.reload:
            command = self.reload(command_name, command.__module__)

        if not command.is_disabled:
            command.run(*args, **kwargs)
