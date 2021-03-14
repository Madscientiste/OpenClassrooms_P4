from app.views import MainView

from .abc import BaseCommand
from app.decorators import sanitize_params


class MainCommand(BaseCommand):
    name = "main"
    usage = "main"
    description = "Shows the main page"
    is_hidden = True

    def __init__(self, cmd_context) -> None:
        super().__init__(current_cmd=self.name)

        self.cmd_context = cmd_context

        self.context = BaseCommand.context.copy()
        self.context["main_view"] = MainView()

    def execute(self, args):
        main_view: MainView = self.context["main_view"]
        main_view.render_main_page(commands=self.cmd_context)
