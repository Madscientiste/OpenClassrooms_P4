import random

from faker import Faker

from .abc import BaseSubCommand


class CreatePlayer(BaseSubCommand):
    name = "create"
    usage = "player create"
    description = "Create a new player"

    def __init__(self, context) -> None:
        super().__init__(context)

        self.fields = [
            {"name": "first_name", "value": None, "special": None},
            {"name": "last_name", "value": None, "special": None},
            {"name": "birthday", "value": None, "special": None},
            {"name": "sexe", "value": None, "special": None},
            {"name": "rank", "value": None, "special": None},
        ]

    def _create_single(self):
        """Create a single player using a questions."""

        for f_index, field in enumerate(self.fields):
            self.player_view.render_questions(self.fields, "Creating a Player")

            f_name = field["name"]
            f_special = field["special"]

            if f_special:
                value = f_special()
            else:
                value = input(f"-> {f_name}: ")

            if not value:
                self.error_view.missing_value(f_name, True)
                value = self._generate_fake(f_name)

            if value == "*":
                value = self._generate_fake(f_name)

            self.fields[f_index]["value"] = value

        params = {field["name"]: field["value"] for field in self.fields}

        new_player = self.player_model(**params)
        new_player = new_player.save()

        self.player_view.render_single_player(new_player, "Created Player")

    def _create_multiple(self):
        """Generate 8 random players"""

        player_list = []

        for i in range(8):
            params = {}

            for field in self.fields:
                f_name = field["name"]

                value = self._generate_fake(f_name)
                params[f_name] = value

            new_player = self.player_model(**params)
            new_player = new_player.save()

            player_list.append(new_player)

        self.player_view.render_multiple_players(player_list, "Registred Players")

    def _generate_fake(self, field):
        """Generate Fake data using a given type"""
        fake = Faker()

        params = {}
        random_rank = random.randint(1, 100)

        params["first_name"] = fake.first_name()
        params["last_name"] = fake.last_name()
        params["birthday"] = fake.date().replace("-", "/")
        params["sexe"] = random.choice(["Male", "Female"])
        params["rank"] = random_rank

        return params[field]

    def execute(self, args):
        """Run the current command"""
        action = args.pop(0) if len(args) else None

        if action == "*":
            self._create_multiple()
        else:
            self._create_single()
