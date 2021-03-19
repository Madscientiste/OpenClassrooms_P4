from texttable import Texttable

from .abc import BaseView


class PlayerView(BaseView):
    def render_multiple_players(self, player_list, title):
        """Renders Multiple Players into a Table."""
        text_table = Texttable()
        self.body = []  # Reset the body to avoid duplicates

        if player_list:
            player_list = player_list.copy()
            header_keys = player_list[0].keys()
            headers = [header for header in header_keys]
            headers = list(set(["id", *headers]))

            player_ids = [id.doc_id for id in player_list]
            players = []

            for index, player_id in enumerate(player_ids):
                player = player_list[index]
                player["id"] = player_id

                players.append([player[key] for key in headers])

            text_table.add_rows([headers, *players])

            table = text_table.draw()

            self.set_title(title)
            self.add_body(table)
        else:
            self.set_title("Error")
            self.add_body("Not Found")

        self.render_view()

    def render_single_player(self, player, title):
        """Renders a single Player into a Table."""
        self.body = []  # Reset the body to avoid duplicates
        text_table = Texttable()

        if player:
            headers = ["id", *[header for header in player.keys()]]

            player["id"] = player.doc_id
            player = [player[key] for key in headers]

            text_table.add_rows([headers, player])

            table = text_table.draw()
            table_width = len(table.split("\n")[0])

            self.set_title(title)
            self.add_body(table)

            print(title.center(table_width, "-"))
            print(table)
        else:
            self.set_title("Error")
            self.add_body("Not Found")

        self.set_footer(" Waiting Input ")
        self.render_view()
