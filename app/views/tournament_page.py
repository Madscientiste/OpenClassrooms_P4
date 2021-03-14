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

    def render_player_selection(self, fields, title):
        self.body = []
        self.set_title(title)

        self.__show_fields(fields)
        self.__show_generator_note()

        self.set_footer("Waiting Input")
        self.render_view()

    def render_created_tournament(self, tournament, title):
        pass