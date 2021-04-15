import os


class BaseView:
    SCREEN_WIDTH = os.get_terminal_size().columns

    SEPARATOR_LENGTH = SCREEN_WIDTH
    SEPARATOR_TOP = "="
    SEPARATOR_BOT = "="

    title = " {} "
    body = []
    footer = " Awaiting Command "

    def _show_fields(self, fields):
        for field in fields:
            if field["name"] == "players" and isinstance(field["value"], list):
                self.add_body(f'-- {field["name"]} : {[player.doc_id for player in field["value"]]}')
            else:
                self.add_body(f'-- {field["name"]} : {field["value"]}')

    def _show_generator_note(self):
        """A Note for the generator of values"""
        self.add_body(" ")
        self.add_body(f" Note ".center(self.SCREEN_WIDTH, "-"))
        self.add_body(" use * as input to generate a random value regarding that field ".center(self.SCREEN_WIDTH, "-"))
        self.add_body(f"".center(self.SCREEN_WIDTH, "-"))

    def _show_tournament(self, tournament):
        players = lambda players: [player["id"] for player in players]

        self.add_body(f"-- id : {tournament.doc_id}")

        for key in tournament.keys():
            if key == "state":
                continue

            if key == "players":
                self.add_body(f"-- {key} : {players(tournament[key])}")
            else:
                self.add_body(f"-- {key} : {tournament[key]}")

    def render_questions(self, fields, title):
        """Render questions using list of fields"""
        self.body = []
        self.set_title(title)

        self._show_fields(fields)
        self._show_generator_note()

        self.set_footer("Waiting Input")
        self.render_view()

    def colorize(self, color_name, text):
        """Colorize a string witha given color"""

        colors = {}
        colors["danger"] = "\033[91m"
        colors["success"] = "\033[92m"
        colors["warning"] = "\033[93m"
        colors["info"] = "\033[94m"

        return colors[color_name] + text + "\033[0m"

    def clear_screen(self):
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def center_item(self, item, char="-", no_space=False):
        """Center an item in the middle of the screen"""
        if no_space:
            return item.center(self.SCREEN_WIDTH, char)
        else:
            return f" {item} ".center(self.SCREEN_WIDTH, char)

    def set_title(self, title):
        """Set the Title."""
        self.title = f" {title} "

    def add_body(self, body):
        """Set the Body."""
        self.body.append(body)

    def set_footer(self, footer):
        """Set the Footer."""
        self.footer = f" {footer} "

    def center_table(self, table):
        """Center a table in the middle of the screen."""
        temp = table.split("\n")
        temp = [v.center(self.SCREEN_WIDTH, " ") for v in temp]
        table = "\n".join(temp)

        return table

    def render_view(self):
        """Render The view."""
        self.clear_screen()

        print(self.title.center(self.SEPARATOR_LENGTH, self.SEPARATOR_TOP))

        print()
        print("\n".join(self.body))
        print()

        print(self.footer.center(self.SEPARATOR_LENGTH, self.SEPARATOR_BOT))
