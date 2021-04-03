from app.views import ErrorView, MainView


class BaseSubCommand:
    name = None
    usage = None
    description = None

    def __init__(self, context) -> None:
        self.context = context

    def _sanitize_args(self):
        pass
