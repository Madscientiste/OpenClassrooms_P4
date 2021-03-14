


from .abc import BaseCommand


class HelpCommand(BaseCommand):
    name = "help"
    usage = "help <command>"
    description = "Get the information about a command"

    def execute(self, args, cmd_context):
        print(cmd_context)
