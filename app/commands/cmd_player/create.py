import re

from InquirerPy.inquirer import text, select
from prompt_toolkit.validation import Validator, ValidationError

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
            if document.text.isdigit():
                raise ValidationError(
                    message="Only numbers are allowed",
                    cursor_position=document.cursor_position,
                )


    def create_multiples(count):
        pass

    # Running the command

    def run(self, context: typings.Context, args: list):
        player_model = context["models"]["Player"]
        player_view = context["views"]["player"]

        questions = {
            "first_name": text(
                message="Enter the first name of the player:",
                validate=self.TextValidator(),
            ),
            "last_name": text(
                message="Enter the last name of the player:",
                validate=self.TextValidator(),
            ),
            "birthday": text(
                message="Enter the birthday of the player:",
                validate=self.DateValidator(),
            ),
            "sexe": select(
                message="Enter the sexe of the player:",
                choices=["male", "female"],
            ),
            "rank": text(
                message="Enter the rank of the player:",
                validate=self.DigitValidator(),
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
