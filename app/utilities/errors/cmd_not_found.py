from .base import BaseError


class CommandNotFound(BaseError):
    """Raised when a command wasn't found"""

    def __init__(self, *args, **kwargs) -> None:
        self.error_view.command_not_found(*args, **kwargs)