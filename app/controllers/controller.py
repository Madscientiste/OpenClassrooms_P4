import os

from app.commands import PlayerCommand, TournamentCommand, HelpCommand, MainCommand, TestCommand
from app.views import MainView

from .handler import Handle


class Controller:
    def __init__(self) -> None:
        self.is_running = True
        self.main_view = MainView()
        self.commands = [PlayerCommand, TournamentCommand, HelpCommand, MainCommand, TestCommand]

    @Handle.exceptions
    def run(self):
        self.main_view.render_main_page(commands=self.commands)

        while self.is_running:
            input_content = input("-> : ")
            args = input_content.split(" ")

            cmd_name = args.pop(0)

            if cmd_name:
                for Command in self.commands:
                    if cmd_name == Command.name:
                        command = Command(cmd_context=self.commands)
                        command.execute(args)

            else:
                print("no input")
