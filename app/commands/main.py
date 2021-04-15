from app.views import MainView

from .abc import BaseCommand
from app.models import Tournament
from app.utilities.handler import CommandHandler


@CommandHandler.register_command
class MainCommand(BaseCommand):
    name = "main"
    usage = "main"
    description = "Shows the main page"
    is_hidden = True

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.cmd_context = cmd_context.values()

        self.context = BaseCommand.context.copy()
        self.context["main_view"] = MainView(None)
        self.context["tournament_model"] = Tournament

    def execute(self, args):
        tournaments = self.context["tournament_model"].find_all()
        self.context["main_view"].render_main_page(self.cmd_context, tournaments)
