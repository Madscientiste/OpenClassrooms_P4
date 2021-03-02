import os

from app.commands import PlayerCommand, TournamentCommand, HelpCommand


class Controller:
    def __init__(self) -> None:
        self.is_running = True
        self.commands = [PlayerCommand, TournamentCommand, HelpCommand]

    def run(self):
        while self.is_running:
            input_content = input("-> : ")
            args = input_content.split(" ")

            os.system("cls" if os.name == "nt" else "clear")

            cmd_name = args.pop(0)

            if cmd_name:
                for Command in self.commands:
                    if cmd_name == Command.name:
                        command = Command()
                        command.execute(args=args, cmd_context=self.commands)

            else:
                print("no input")