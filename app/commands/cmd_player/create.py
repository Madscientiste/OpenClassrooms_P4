import re
import random

from InquirerPy.inquirer import text, select
from prompt_toolkit.validation import Validator, ValidationError
from faker import Faker

from datetime import datetime
from app.commands.base import BaseCommand
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "create"
    usage = "player create"
    description = "Create a new player"

    # Error Handling

    class DateValidator(Validator):
        def validate(self, document):
            try:
                datetime.strptime(document.text, "%d/%m/%Y")
            # flake8: noqa
            except:
                raise ValidationError(
                    message="Date is in the wrong format, it should be : DD/MM/YYYY",
                    cursor_position=document.cursor_position,
                )

    class TextValidator(Validator):
        def validate(self, document):
            if re.search(r"\d", document.text):
                raise ValidationError(
                    message="This input contains numeric characters",
                    cursor_position=document.cursor_position,
                )

    class DigitValidator(Validator):
        def validate(self, document):
            if not document.text.isdigit():
                raise ValidationError(
                    message="Only numbers are allowed",
                    cursor_position=document.cursor_position,
                )

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

        rand_count = self.pop_arg(args)
        if rand_count.isdigit():
            total_created = self.create_multiples(rand_count, player_model)
            return player_view.render_multiples(total_created, title="Created Players")

        questions = {
            "first_name": text(
                message="Enter the first name of the player:",
                validate=self.TextValidator(),
                default=f'{self._generate_fake("first_name")}',
            ),
            "last_name": text(
                message="Enter the last name of the player:",
                validate=self.TextValidator(),
                default=f'{self._generate_fake("last_name")}',
            ),
            "birthday": text(
                message="Enter the birthday of the player:",
                validate=self.DateValidator(),
                default=f'{self._generate_fake("birthday")}',
            ),
            "sexe": select(
                message="Enter the sexe of the player:",
                choices=["male", "female"],
                default=f'{self._generate_fake("sexe")}',
            ),
            "rank": text(
                message="Enter the rank of the player:",
                validate=self.DigitValidator(),
                default=f'{self._generate_fake("rank")}',
            ),
        }

        result = {}

        for key, value in questions.items():
            response = value.execute()

            if not response:
                raise errors.GenericError("Misconstructed input")

            result[key] = response

        new_player = player_model(**result)
        new_player = new_player.save()

        player_view.render_single(new_player, title="Created Player")
