import random

from faker import Faker

from app.views import ErrorView, MainView


class BaseSubCommand:
    name = None
    usage = None
    description = None

    def __init__(self, context) -> None:
        self.player_model = context["player_model"]
        self.tournament_model = context["tournament_model"]
        self.sub_commands = context["sub_commands"]

        self.player_view = context["player_view"]
        self.tournament_view = context["tournament_view"]
        self.error_view = context["error_view"]
        self.main_view = context["main_view"]

    def _generate_fake(self, field):
        """Generate Fake data using a given type"""
        fake = Faker()

        params = {}
        random_turns = random.randint(1, 4)

        params["name"] = fake.name()
        params["players"] = [i for i in range(8)]

        params["location"] = ", ".join(fake.address().split("\n"))
        params["date"] = fake.date().replace("-", "/")
        params["turns"] = random_turns
        params["time_control"] = random.choices(["blitz", "bullet"])
        params["description"] = fake.paragraph(nb_sentences=1)

        return params[field]
