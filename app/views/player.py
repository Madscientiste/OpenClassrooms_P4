from .base import BaseView

from app.models import database


class View(BaseView):
    """Player View
    Can render anything related to the player
    """

    def render_single(self, player: database.Player, title: str):
        self.reset_values()
        self.set_title(title)

        player: dict = player.to_dict()
        header: list = player.keys()

        header_size = len(header)
        self.fluidify_table(header_size)
        self.center_cols_items(header_size)

        self.text_table.add_rows([header, player.values()])

        table = self.text_table.draw()
        table = self.center_table(table)

        self.add_body(table)
        self.render_view()

    def render_multiples(self, players: list[database.Player], title: str, sort_by="id"):
        self.reset_values()
        self.set_title(title)

        players: list = sorted([database.Player.to_dict(x) for x in players], key=lambda k: k[sort_by])
        header: list = vars(database.Player()).keys()

        header_size = len(header)
        self.fluidify_table(header_size)
        self.center_cols_items(header_size)

        self.text_table.add_row(header)

        for player in players:
            self.text_table.add_row(player.values())

        table = self.text_table.draw()
        table = self.center_table(table)

        self.add_body(table)
        self.render_view()
