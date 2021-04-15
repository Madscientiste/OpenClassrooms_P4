from texttable import Texttable
from .abc import BaseView


class TournamentView(BaseView):
    def _show_commands(self, commands):
        self.add_body(" ")
        for command_name in commands:
            cols = 8
            size = self.SCREEN_WIDTH // cols

            cmd_name = command_name.ljust(size, " ")
            cmd_desc = commands[command_name].__doc__.ljust(size, " ")

            self.add_body(f"--> {cmd_name}{cmd_desc}")

    def _show_matches(self, matches):
        space = self.SCREEN_WIDTH // 2

        self.add_body(f"{'[ID]'.ljust(space, ' ')}{'SCORE'.rjust(space, ' ')}")

        for match_id in matches.keys():
            players = matches[match_id]

            p1 = players[0]
            p2 = players[1]

            right_side = f'{p1["points"]} - {p2["points"]}'.rjust(space, " ")

            if p1["points"] and p2["points"] == 0.5:
                right_side = self.colorize("warning", "DRAW!".rjust(space, " "))

            match_id = match_id.center(2, " ")
            left_side = f'[{match_id}] --> {p1["first_name"]} < VS > {p2["first_name"]}'.ljust(space, " ")

            self.add_body(f"{left_side}{right_side}")

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

    def render_created_tournament(self, tournament, title):
        self.body = []
        self.set_title(title)

        self._show_tournament(tournament)

        self.add_body(" ")
        self.add_body(self.center_item("Note"))
        self.add_body(" ")

        command = self.colorize("success", f"tournament start {tournament.doc_id}")
        self.add_body(f"---> To run the tournament type: {command}")

        self.render_view()

    def render_all_tournaments(self, tournaments, title):
        self.body = []
        self.set_title(title)

        for index, tournament in enumerate(tournaments):
            index += 1  # Caveat

            self.add_body(f"----> Tournament {index} of {len(tournaments)}")
            self._show_tournament(tournament)
            self.add_body(" ")

        self.add_body(self.center_item("NOTE"))
        self.add_body(" ")
        command = self.colorize("success", f"tournament start {self.colorize('warning', '<tournament_id>')}")
        self.add_body(f"---> To start/resume a tournament type: {command}")

        self.render_view()

    def render_tournament(self, tournament, matches, commands):
        self.body = []
        self.set_title(tournament["name"])

        self._show_tournament(tournament)

        self.add_body(" ")
        self.add_body(self.center_item("Round"))
        self.add_body(" ")

        self._show_matches(matches)

        self.add_body(" ")
        self.add_body(self.center_item("Available Commands"))
        self._show_commands(commands)

        self.render_view()

    def render_match(self, match):
        self.body = []

        self.set_title("Match")

        player1 = match[0]
        player2 = match[1]

        self.add_body(f"- 1 if {player1['first_name']} has won")
        self.add_body(f"- 2 if {player2['first_name']} has won")
        self.add_body(f"- * if its a draw")
        self.add_body(f"- - to go back")

        self.set_footer("Waiting Input")

        self.render_view()