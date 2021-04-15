from app.views import ErrorView, MainView


class BaseSubCommand:
    name = None
    usage = None
    description = None

    def __init__(self, context) -> None:
        self.player_model = context["player_model"]
        self.sub_commands = context["sub_commands"]

        self.player_view = context["player_view"]
        self.error_view = context["error_view"]
        self.main_view = context["main_view"]
