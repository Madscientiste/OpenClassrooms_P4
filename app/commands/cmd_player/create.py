import random
from datetime import datetime

from InquirerPy.inquirer import text, select
from faker import Faker

from app.commands.base import BaseCommand
from app.utilities import typings, errors, validators


class Command(BaseCommand):
    name = "create"
    usage = "player create"
    description = "Create a new player"

    def _generate_fake(self, field, all=False) -> str:
        """Generate Fake data using a given type"""
        fake = Faker()

        params = {}
        random_rank = random.randint(1, 100)
        random_date = datetime.strptime(fake.date(), "%Y-%m-%d").date()

        params["first_name"] = fake.first_name()
        params["last_name"] = fake.last_name()
        params["birthday"] = random_date.strftime("%d/%m/%Y")
        params["sexe"] = random.choice(["Male", "Female"])
        params["rank"] = random_rank

        return params[field] if not all else params

    def create_multiples(self, count, player_model):
        total_created = []

        for x in range(int(count)):
            fake_player = self._generate_fake(None, True)

            new_player = player_model(**fake_player)
            new_player = new_player.save()
            total_created.append(new_player)

        return total_created

    # Running the command

    def run(self, context: typings.Context, args: list):
        player_model = context["models"]["Player"]
        player_view = context["views"]["player"]

        player_count = self.pop_arg(args)
        if player_count and player_count.isdigit():
            total_created = self.create_multiples(player_count, player_model)
            return player_view.render_multiples(total_created, title="Created Players")

        questions = {
            "first_name": text(
                message="Enter the first name of the player:",
                validate=validators.TextValidator(),
                default=f'{self._generate_fake("first_name")}',
            ),
            "last_name": text(
                message="Enter the last name of the player:",
                validate=validators.TextValidator(),
                default=f'{self._generate_fake("last_name")}',
            ),
            "birthday": text(
                message="Enter the birthday of the player:",
                validate=validators.DateValidator(),
                default=f'{self._generate_fake("birthday")}',
            ),
            "sexe": select(
                message="Enter the sexe of the player:",
                choices=["male", "female"],
                default=f'{self._generate_fake("sexe")}',
            ),
            "rank": text(
                message="Enter the rank of the player:",
                validate=validators.DigitValidator(),
                default=f'{self._generate_fake("rank")}',
            ),
        }

        result = {}

        for key, value in questions.items():
            sanitize_value = type(getattr(player_model(), key))
            try:
                result[key] = sanitize_value(value.execute())
            except KeyboardInterrupt:
                raise errors.GenericError("Canceld the creation of the player", title="Note")

        new_player = player_model(**result)
        new_player = new_player.save()

        player_view.render_single(new_player, title="Created Player")
