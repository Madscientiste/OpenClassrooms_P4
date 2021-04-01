from texttable import Texttable
from .abc import BaseView


class TournamentView(BaseView):
    def render_player_selection(self, players, fields, title):
        text_table = Texttable()

        self.body = []
        self.set_title(title)

        self._show_fields(fields)
        self._show_generator_note()

        self.add_body("")
        self.add_body(self.center_item(title))

        players = players.copy()
        header_keys = players[0].keys()
        headers = [header for header in header_keys]
        headers = list(dict.fromkeys(["id", *headers]))

        player_ids = [id.doc_id for id in players]
        rows = []

        for index, player_id in enumerate(player_ids):
            player = players[index]
            player["id"] = player_id

            rows.append([player[key] for key in headers])

        text_table.add_rows([headers, *rows])
        table = text_table.draw()
        table = self.center_table(table)

        self.add_body(table)
        self.set_footer("Waiting Input")
        self.render_view()

    def render_created_tournament(self, fields, title):
        self.body = []
        self.set_title(title)

        self._show_fields(fields)
        self.render_view()