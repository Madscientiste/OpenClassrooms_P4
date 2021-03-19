from app.views import MainView
from app.utilities.handler import CommandHandler


class Controller:
    def __init__(self) -> None:
        self.is_running = True
        self.main_view = MainView(None)
        self.command_handler = CommandHandler(blacklist=["__init__", "abc"])

    # @Handle.exceptions
    def run(self):
        self.command_handler.import_commands("app.commands")
        commands = self.command_handler.COMMANDS

        self.main_view.render_main_page(commands)

        while self.is_running:
            input_content = input("-> : ")
            args = input_content.split(" ")

            cmd_name = args.pop(0)

            if cmd_name:
                for Command in commands:
                    if cmd_name == Command.name:
                        command = Command(cmd_context=commands)
                        command.execute(args)

            else:
                print("no input")
