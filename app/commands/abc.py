from app.views import ErrorView


class BaseCommand:
    name = None
    usage = None
    description = None
    is_hidden = False
    
    sub_commands = {}
    context = {}
    
    def __init__(self, current_cmd) -> None:
        self.context["error_view"] = ErrorView(current_cmd)


    def execute(self, args):
        pass

    def execute_sub(self, sub_cmd, *args, **kwargs):
        sub_cmd = self.sub_commands.get(sub_cmd)

        if not sub_cmd:
            return None

        sub_cmd(*args, **kwargs)
