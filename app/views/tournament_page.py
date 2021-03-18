from texttable import Texttable
from .abc import BaseView


class TournamentView(BaseView):
    def __show_fields(self, fields):
        for field in fields:
            self.add_body(f'-- {field["name"]} : {field["value"]}')

    def __show_generator_note(self):
        self.add_body(" ")
        self.add_body(f" Note ".center(self.SCREEN_WIDTH, "-"))
        self.add_body(" use * as input to generate a random value regarding that field ".center(self.SCREEN_WIDTH, "-"))
        self.add_body(f"".center(self.SCREEN_WIDTH, "-"))

    def render_questions(self, fields, title):
        self.body = []
        self.set_title(title)

        self.__show_fields(fields)
        self.__show_generator_note()

        self.set_footer("Waiting Input")
        self.render_view()

    def render_player_selection(self, players, fields, title):
        text_table = Texttable()

        self.body = []
        self.set_title(title)

        self.__show_fields(fields)
        self.__show_generator_note()

        self.add_body("")
        self.add_body(title.center(self.SCREEN_WIDTH, "-"))

        players = players.copy()
        header_keys = players[0].keys()
        headers = [header for header in header_keys]
        headers = list(set(["id", *headers]))

        player_ids = [id.doc_id for id in players]
        rows = []

        for index, player_id in enumerate(player_ids):
            player = players[index]
            player["id"] = player_id

            rows.append([player[key] for key in headers])

        text_table.add_rows([headers, *rows])
        table = text_table.draw()

        # doing fancy stuff
        temp = table.split("\n")
        temp = [v.center(self.SCREEN_WIDTH, " ") for v in temp]
        table = "\n".join(temp)

        self.add_body(table)
        self.set_footer("Waiting Input")
        self.render_view()

    def render_created_tournament(self, title):
        pass