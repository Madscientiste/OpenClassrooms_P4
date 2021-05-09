from prompt_toolkit.validation import Validator, ValidationError


class DigitValidator(Validator):
    def validate(self, document):
        if not document.text.isdigit():
            raise ValidationError(
                message="Only numbers are allowed",
                cursor_position=document.cursor_position,
            )
        elif not document.text:
            raise ValidationError(
                message="Input cannot be left empty",
                cursor_position=document.cursor_position,
            )
