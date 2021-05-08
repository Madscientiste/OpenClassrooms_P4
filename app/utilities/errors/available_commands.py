from .base import BaseError


class AvailableCommands(BaseError):
    """its NOT an arror, but a way to render the commands without having to code a lot"""

    def __init__(self, *args, **kwargs) -> None:
        self.main_view.render_available_commands(*args, **kwargs)
