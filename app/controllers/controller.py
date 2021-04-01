from app.views import MainView, ErrorView
from app.utilities.handler import CommandHandler, ExecptionHandler


class Controller:
    def __init__(self) -> None:
        self.is_running = True
        self.main_view = MainView(None)
        self.error_view = ErrorView()

        self.command_handler = CommandHandler(blacklist=["__init__", "abc"])

    @ExecptionHandler.keyboard_interrupt
    def run(self):
        self.command_handler.import_commands("app.commands")
        commands = self.command_handler.COMMANDS.values()

        self.main_view.render_main_page(commands)

        while self.is_running:
            input_content = input("-> : ").strip()
            args = input_content.split(" ")

            cmd_name = args.pop(0)

            context = {}
            context["error_view"] = self.error_view
            context["main_view"] = self.main_view

            if cmd_name:
                self.command_handler.execute(cmd_name, args, context)
            else:
                self.error_view.generic_error(message="No input given", centered=True)
                self.main_view.render_main_page(commands)
