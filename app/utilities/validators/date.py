# flake8: noqa

from datetime import datetime
from prompt_toolkit.validation import Validator, ValidationError

class DateValidator(Validator):
    def validate(self, document):
        try:
            datetime.strptime(document.text, "%d/%m/%Y")
        except:
            raise ValidationError(
                message="Date is in the wrong format, it should be : DD/MM/YYYY",
                cursor_position=document.cursor_position,
            )
        
        if not document.text:
            raise ValidationError(
                message="Input cannot be left empty",
                cursor_position=document.cursor_position,
            )
