import re

from prompt_toolkit.validation import Validator, ValidationError


class TextValidator(Validator):
    def validate(self, document):
        if re.search(r"\d", document.text):
            raise ValidationError(
                message="This input contains numeric characters",
                cursor_position=document.cursor_position,
            )
        elif not document.text:
            raise ValidationError(
                message="Input cannot be left empty",
                cursor_position=document.cursor_position,
            )
