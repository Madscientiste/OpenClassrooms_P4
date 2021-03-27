import sys
import importlib
from importlib import resources


class CommandHandler:
    """Load commands from a package"""

    COMMANDS = {}

    def __init__(self, blacklist) -> None:
        self.blacklist = blacklist

    def import_commands(self, cmd_package):
        files = resources.contents(cmd_package)
        commands = [f[:-3] for f in files if f.endswith(".py")]
        commands = [command for command in commands if command not in self.blacklist]

        for command in commands:
            importlib.import_module(f"{cmd_package}.{command}")

        return commands

    def reload(self, package):
        module = sys.modules[package]
        importlib.reload(module)

    def execute(self, command_name, args, context):
        CommandClass = self.COMMANDS.get(command_name)

        if CommandClass:
            command_package = CommandClass.__module__
            self.reload(command_package)

            CommandClass = self.COMMANDS.get(command_name)
            command = CommandClass(cmd_context=self.COMMANDS)
            command.execute(args)
        else:
            context["error_view"].generic_error(message=f"Command [{command_name}] doesn't exist", centered=True)
            context["main_view"].render_main_page(self.COMMANDS.values())

    @classmethod
    def register_command(cls, command):
        cls.COMMANDS[command.name] = command
