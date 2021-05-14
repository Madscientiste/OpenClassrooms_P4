# flake8: noqa

import random
from datetime import datetime

from InquirerPy.inquirer import text, select
from faker import Faker

from app.commands.base import BaseCommand
from app.utilities import typings, errors, validators


class Command(BaseCommand):
    name = "create"
    usage = "tournament create"
    description = "Create a new tournament"

    def _generate_fake(self, field):
        """Generate Fake data using a given type"""
        fake = Faker()

        params = {}
        random_turns = random.randint(1, 4)
        random_date = datetime.strptime(fake.date(), "%Y-%m-%d").date()

        params["name"] = fake.name()
        params["location"] = ", ".join(fake.address().split("\n"))
        params["date"] = random_date.strftime("%d/%m/%Y")
        params["turns"] = random_turns
        params["time_control"] = random.choices(["blitz", "bullet"])
        params["description"] = fake.paragraph(nb_sentences=1)

        return params[field]

    def run(self, context: typings.Context, args: list):
        tournament_model = context["models"]["Tournament"]
        tournament_view = context["views"]["tournament"]

        players = context["models"]["Player"].find_many()

        has_min_players = lambda players: len(players) >= 8

        if not has_min_players(players):
            raise errors.GenericError("Cannot create a tournament without at least 8 players created !")

        questions = {
            "name": text(
                message="Enter the name of the tournament:",
                validate=validators.TextValidator(),
                default=f'{self._generate_fake("name")}',
            ),
            "location": text(
                message="Enter the location of the tournament:",
                validate=lambda text: len(text) > 0,
                default=f'{self._generate_fake("location")}',
            ),
            "date": text(
                message="Enter date of the tournament:",
                validate=validators.DateValidator(),
                default=f'{self._generate_fake("date")}',
            ),
            "rounds": text(
                message="Enter the rounds of the tournament:",
                validate=validators.DigitValidator(),
                default="4",
            ),
            "players": select(
                message="Select the participants:",
                choices=[{"name": f"{p.full_name}", "value": p} for p in players],
                instruction="> use Spacebar to select, and Enter to exit the selection",
                validate=lambda players: has_min_players(players) and len(players) % 2 == 0 and len(players),
                invalid_message="Cannot select less than 4 players or odd players",
                multiselect=True,
                transformer=lambda result: "%s player%s selected" % (len(result), "s" if len(result) > 1 else ""),
            ),
            "time_control": select(
                message="Time control of the Tournament:",
                choices=["blitz", "bullet"],
                default="blitz",
            ),
            "desc": text(
                message="Description:",
                default="None",
            ),
        }

        result = {}

        for key, value in questions.items():
            sanitize_value = type(getattr(tournament_model(), key))
            try:
                result[key] = sanitize_value(value.execute())
            except KeyboardInterrupt:
                raise errors.GenericError("Canceld the creation of the tournament", title="Note")

        new_tournament = tournament_model(**result)
        new_tournament = new_tournament.save()

        tournament_view.render_single(new_tournament, title="Created Tournament", hint=True)
