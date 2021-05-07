from .base import BaseError


class GenericError(BaseError):
    """Get called when ANYTHING get raised with the `Exception` class"""

    def __init__(self, *args, **kwargs) -> None:
        self.error_view.generic_error(*args, **kwargs)