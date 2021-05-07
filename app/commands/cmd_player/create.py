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

    def _validate_date(*args, **kwargs):
        class DateValidator(Validator):
            def validate(self, document):
                try:
                    datetime.strptime(document.text, "%d/%m/%Y")
                except:
                    raise ValidationError(
                        message="Date is in the wrong format, it should be : DD/MM/YYYY",
                        cursor_position=document.cursor_position,
                    )

        return DateValidator()

    def _validate_text(*args, **kwargs):
        class TextValidator(Validator):
            def validate(self, document):
                if re.search(r"\d", document.text):
                    raise ValidationError(
                        message="This input contains numeric characters",
                        cursor_position=document.cursor_position,
                    )

        return TextValidator()

    def _validate_digit(*args, **kwargs):
        class DigitValidator(Validator):
            def validate(self, document):
                if document.text.isdigit():
                    raise ValidationError(
                        message="Only numbers are allowed",
                        cursor_position=document.cursor_position,
                    )

        return DigitValidator()

    # Running the command

    def create_multiples(count):
        pass

    def run(self, context: typings.Context, args: list):
        player_model = context["models"]["Player"]
        player_view = context["views"]["player"]

        questions = {
            "first_name": text(
                message=f"Enter the first name of the player:",
                validate=self._validate_text(),
                validate_while_typing=True,
            ),
            "last_name": text(
                message=f"Enter the last name of the player:",
                validate=self._validate_text(),
            ),
            "birthday": text(
                message=f"Enter the birthday of the player:",
                validate=self._validate_date(),
            ),
            "sexe": select(
                message=f"Enter the sexe of the player:",
                choices=["male", "female"],
            ),
            "rank": text(
                message=f"Enter the rank of the player:",
                validate=self._validate_digit(),
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