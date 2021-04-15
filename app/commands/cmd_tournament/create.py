import random

from .abc import BaseSubCommand


class CreateTournament(BaseSubCommand):
    name = "create"
    usage = "tournament create"
    description = "Create a new tournament"

    def __init__(self, context) -> None:
        super().__init__(context)

        self.fields = [
            {"name": "name", "value": None, "special": None},
            {"name": "location", "value": None, "special": None},
            {"name": "date", "value": None, "special": None},
            {"name": "turns", "value": None, "special": None},
            {"name": "players", "value": None, "special": self._select_players},
            {"name": "time_control", "value": None, "special": None},
            {"name": "description", "value": None, "special": None},
        ]

    def _select_players(self):
        """Handle player selections, return a list of players"""

        selected_players = []

        id_list = lambda: [p.doc_id for p in selected_players]
        players = self.player_model.find_many(None, None)

        if not players:
            self.error_view.generic_error(f"Can't create a tournament, no players registred")
            return 1

        if len(players) < 8:
            self.error_view.generic_error(f"Can't create a tournament with less than 8 players")
            return 1

        self.tournament_view.render_player_selection(players, self.fields, "Available Player(s)")

        while len(selected_players) != 8:
            player_list = [p for p in players if p.doc_id not in id_list()]
            self.tournament_view.render_player_selection(player_list, self.fields, "Available Player(s)")

            print("Selected players:", [p["first_name"] for p in selected_players])

            value = input("Please select a player by its ID: ")

            if value == "*":  # Generate random data regarding that field
                value = str(random.choice([idx.doc_id for idx in player_list]))

            elif value == "-":  # Delete the last player
                if not len(selected_players):
                    self.error_view.generic_error(f"Can't remove last player, list is empty")
                    continue

                deleted = selected_players.pop()
                self.error_view.generic_error(f"{deleted['first_name']} has been remouved from the list")
                continue

            if not value:
                self.error_view.generic_error("No input given")
                continue

            if not value.isdigit():
                self.error_view.generic_error("Only Numbers are allowed")
                continue

            player = self.player_model.find_one(id=int(value))

            if not player:
                self.error_view.generic_error(f"Player with ID [{value}] doesn't exist")
                continue

            if player.doc_id in id_list():
                self.error_view.generic_error("Player already added to the list")
                continue

            player["id"] = player.doc_id
            selected_players.append(player)

        self.tournament_view.render_player_selection(selected_players, self.fields, "Selected Players")
        input("Press enter to continue...")

        return selected_players

    def execute(self, args):
        """Execution of the current command"""

        for f_index, field in enumerate(self.fields):
            self.tournament_view.render_questions(self.fields, "Creating a Tournament")

            f_name = field["name"]
            f_special = field["special"]

            if f_special:
                value = f_special()
            else:
                value = input(f"-> {f_name}: ")

            if not value:
                err_message = f"Missing value for : {f_name}\nvalue has been randomized."
                self.error_view.generic_error(message=err_message)
                value = self._generate_fake(f_name)

            if value == "*":
                value = self._generate_fake(f_name)

            elif value == 1:
                self.error_view.generic_error(f"The creation of the tournament has been canceled")
                self.main_view.display_actions(actions=self.sub_commands)
                return

            self.fields[f_index]["value"] = value

        params = {field["name"]: field["value"] for field in self.fields}

        new_tournament = self.tournament_model(**params)
        new_tournament = new_tournament.save()

        self.tournament_view.render_created_tournament(new_tournament, "Created Tournament")
