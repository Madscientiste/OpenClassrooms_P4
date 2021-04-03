import sys
import importlib
from importlib import resources

from app.views import ErrorView, MainView


class BaseCommand:
    name = None
    usage = None
    description = None
    is_hidden = False

    sub_commands = {}
    context = {}

    def __init__(self, current_cmd) -> None:
        self.context["error_view"] = ErrorView()
        self.context["main_view"] = MainView(current_cmd)
        self.current_cmd = current_cmd

    def _reload_sub(self, package):
        module = sys.modules[package]
        importlib.reload(module)

    def sanitize_args():
        pass

    def execute_sub(self, sub_cmd_name, args):
        error_view = self.context["error_view"]
        main_view = self.context["main_view"]

        SubCommand = self.sub_commands.get(sub_cmd_name)

        if not SubCommand:
            error_view.generic_error(f"Sub command [{sub_cmd_name}] in [{self.current_cmd}] doesn't exist")
            main_view.display_actions(self.sub_commands)
            return

        # Dev Purpose
        command_package = SubCommand.__module__
        self._reload_sub(command_package)

        command = SubCommand(context=self.context)
        command.execute(args)