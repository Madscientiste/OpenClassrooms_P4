from app.controllers import Commands, Views
from app.utilities import errors, typings
from app.models import database, other


class MainController:
    def __init__(self) -> None:
        self.is_running = True

        self.commands = Commands(package="app.commands")
        self.views = Views(package="app.views")

        self.models: typings.Models = {
            "Tournament": database.Tournament,
            "Player": database.Player,
            "Round": other.Round,
            "Match": other.Match,
        }

        self.context: typings.Context = {
            "models": self.models,
            "views": self.views,
        }

    def run(self):
        main_view = self.views["main"]

        all_tournaments = lambda: self.models["Tournament"].find_many()
        all_states = lambda: database.State.find_many()

        all_commands = self.commands.cache.values()

        main_view.render_main_page(all_commands, all_tournaments(), all_states())

        try:
            while self.is_running:
                try:
                    input_content = input("-> : ").strip()
                    args = input_content.split(" ")

                    command_name = args.pop(0)
                    self.commands.execute(command_name, args=args, context=self.context)

                except Exception as e:
                    if not hasattr(e, "custom"):
                        errors.GenericError(e)

                    main_view.render_main_page(all_commands, all_tournaments(), all_states())

        except KeyboardInterrupt:
            main_view.application_quit()


if __name__ == "__main__":
    app = MainController()
    app.run()
