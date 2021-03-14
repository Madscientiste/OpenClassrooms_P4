import os
from typing import final


class BaseView:
    SCREEN_WIDTH = os.get_terminal_size().columns
    
    SEPARATOR_LENGTH = SCREEN_WIDTH
    SEPARATOR_TOP = "="
    SEPARATOR_BOT = "="
    
    title = " {} "
    body = []
    footer = " {} "

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
        self.footer = self.footer.format(footer)

    def render_view(self):
        """Render The view."""
        self.clear_screen()

        print(self.title.center(self.SEPARATOR_LENGTH, self.SEPARATOR_TOP))

        print()
        print("\n".join(self.body))
        print()

        print(self.footer.center(self.SEPARATOR_LENGTH, self.SEPARATOR_BOT))
