from app.utilities import typings, errors


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

    def _run(self, context: typings.Context, args: list):
        """Run sub commands and handle the error if there is any on execution"""
        try:
            main_view = context["views"]["main"]

            sub_commands = self.commands.cache.values()
            main_view.render_available_commands(sub_commands)

            command_name = args.pop(0) if args else None
            self.commands.execute(command_name, args=args, context=context)

        except Exception as e:
            if not hasattr(e, "custom"):
                errors.GenericError(e)

            main_view.render_available_commands(sub_commands)
