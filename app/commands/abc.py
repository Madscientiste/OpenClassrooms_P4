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

    def execute_sub(self, sub_cmd_name, *args, **kwargs):
        sub_cmd = self.sub_commands.get(sub_cmd_name)

        if not sub_cmd:
            self.context["error_view"].generic_error(f"Sub command [{sub_cmd_name}] in [{self.current_cmd}] doesn't exist")
            self.context["main_view"].display_actions(self.sub_commands)
            return
            
        sub_cmd(*args, **kwargs)
