import os
from typing import final


class BaseView:
    SCREEN_WIDTH = os.get_terminal_size().columns

    SEPARATOR_LENGTH = SCREEN_WIDTH
    SEPARATOR_TOP = "="
    SEPARATOR_BOT = "="

    title = " {} "
    body = []
    footer = " Waiting Input "

    def clear_screen(self):
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def set_title(self, title):
        """Set the Title."""
        self.title = self.title.format(title)

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
