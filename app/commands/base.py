from app.utilities import typings


class BaseCommand:
    name = None
    usage = None
    description = None

    is_hidden = False
    is_disabled = False
    reload = True

    def pop_arg(self, args) -> str:
        """Pop the first element in a list, return none if the list is empty"""
        return args.pop(0) if args else None

    def run(context: typings.Context, args: list):
        pass
