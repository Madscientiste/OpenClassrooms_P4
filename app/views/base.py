import os

from texttable import Texttable
from app.models import database


class BaseView:
    """BaseView... """

    SCREEN_WIDTH = os.get_terminal_size().columns

    SEPARATOR_LENGTH = SCREEN_WIDTH
    SEPARATOR_TOP = "="
    SEPARATOR_BOT = "="

    text_table = Texttable(max_width=SCREEN_WIDTH)
    text_table.set_chars(["-", "|", "+", "="])

    title = ""
    body = []
    footer = " Waiting Command "

    # -------------------------------
    # Reusable on multiples vies
    # -------------------------------

    def show_generator_note(self):
        """A Note for the generator of values"""
        self.add_body(" ")
        self.add_body(self.center_item(f"Note"))
        self.add_body(self.center_item("use * as input to generate a random value regarding that field"))
        self.add_body(self.center_item("", char="-"))

    def show_commands(self, commands: list):
        for command in commands:
            if command.is_disabled or command.is_hidden:
                continue

            for field in ["name", "usage", "description"]:
                self.add_body(f"-- {field} : {getattr(command, field)}")

            self.add_body("-" * 50)
            self.add_body(" ")

    def show_tournament(self, tournament: database.Tournament):
        for key, value in tournament.to_dict().items():
            if key == "round_instances":
                self.add_body(f"-- {key} : ")

                for index, round in enumerate(value):
                    index += 1

                    timestamp = f"Started on : {round['start_date']} / Ended on : {round['end_date']}"
                    self.add_body(f"---- Round {index} / {timestamp}")

                    for match in round["matches"]:
                        player1 = match["player1"]["first_name"]
                        player2 = match["player2"]["first_name"]
                        colorize = lambda text: self.colorize("warning", text)

                        if match["winner"]:
                            winner = match["winner"]

                            if type(winner) == dict:
                                end_text = colorize("- WINNER")
                                if winner["first_name"] == player1:
                                    self.add_body(f"----- : {colorize(player1)} vs {player2} {end_text}")
                                else:
                                    self.add_body(f"----- : {player1} vs {colorize(player2)} {end_text}")
                            else:
                                self.add_body(f"----- : {player1} vs {player2} {self.colorize('info','- TIE')}")
                        else:
                            self.add_body(f"----- : {player1} vs {player2}")

                    self.add_body(f"")

            elif key == "players":
                self.add_body(f"-- {key} : {[player['first_name'] for player in value]}")

            else:
                self.add_body(f"-- {key} : {value}")

    # # -------------------------------
    # Class Methods
    # -------------------------------

    @classmethod
    def colorize(cls, color_name: str, text: str) -> str:
        """Colorize a string witha given color"""
        colors = {}
        colors["danger"] = "\033[91m"
        colors["success"] = "\033[92m"
        colors["warning"] = "\033[93m"
        colors["info"] = "\033[94m"

        return colors[color_name] + text + "\033[0m"

    @classmethod
    def clear_screen(cls):
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def center_item(cls, item: str, char=" ", no_space=False, is_colored=False) -> str:
        """Center an item in the middle of the screen"""

        width = cls.SCREEN_WIDTH + (0 if not is_colored else 8)
        item = item if no_space else f" {item} "

        return item.center(width, char)

    # -------------------------------
    # TextTable modificators
    # -------------------------------

    @classmethod
    def center_table(cls, table):
        """Center a table in the middle of the screen."""
        temp = table.split("\n")
        temp = [v.center(cls.SCREEN_WIDTH, " ") for v in temp]
        table = "\n".join(temp)

        return table

    def center_cols_items(self, header_size):
        """Center items inside the cols"""
        cols_align = ["c" for _ in range(header_size)]
        self.text_table.set_cols_align(cols_align)

    def fluidify_table(self, header_size):
        """Make table almost fullwith"""
        cols_size = [(self.SCREEN_WIDTH // header_size) - 5 for _ in range(header_size)]
        self.text_table.set_cols_width(cols_size)

    # -------------------------------
    # Private Functions only o be used inside the class
    # -------------------------------

    def set_title(self, title):
        """Set the Title."""
        self.title = f" {title} "

    def add_body(self, body):
        """Set the Body."""
        self.body.append(body)

    def set_footer(self, footer):
        """Set the Footer."""
        self.footer = f" {footer} "

    def reset_values(self):
        """Set default values."""
        self.title = ""
        self.body.clear()
        self.footer = " Waiting Command "
        self.text_table.reset()

    def render_view(self, wait=False):
        self.clear_screen()

        print(self.center_item(self.title, char=self.SEPARATOR_TOP))
        print()
        print("\n".join(self.body))
        print()
        print(self.center_item(self.footer, char=self.SEPARATOR_BOT))

        self.reset_values()

        if wait:
            input()
