


from .abc import BaseCommand


class HelpCommand(BaseCommand):
    name = "help"

    def execute(self, args, cmd_context):
        print(cmd_context)
