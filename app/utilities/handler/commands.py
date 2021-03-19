import importlib
from importlib import resources


class CommandHandler:
    """Load commands from a package"""

    COMMANDS = []

    def __init__(self, blacklist) -> None:
        self.blacklist = blacklist

    def import_commands(self, cmd_package):
        files = resources.contents(cmd_package)
        commands = [f[:-3] for f in files if f.endswith(".py")]
        commands = [command for command in commands if command not in self.blacklist]

        for command in commands:
            importlib.import_module(f"{cmd_package}.{command}")

        return commands

    @classmethod
    def register_command(cls, command):
        cls.COMMANDS.append(command)