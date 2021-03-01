import os
from typing import final


class BaseView:
    SEPARATOR_LENGTH = 50
    SEPARATOR_TOP = "-" * SEPARATOR_LENGTH
    SEPARATOR_BOT = "=" * SEPARATOR_LENGTH

    top = []
    mid = []
    bot = []

    final = [
        "\n".join(top),
        "\n".join(mid),
        "\n".join(bot),
    ]

    def clear_screen(self):
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def set_top(self, data):
        self.top.append(data)

    def set_mid(self, data):
        self.mid.append(data)

    def set_bot(self, data):
        self.bot.append(data)

    def render_view(self):
        print("\n".join(self.final))
