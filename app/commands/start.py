from .base import BaseCommand

from app.controllers import Commands
from app.utilities import typings, errors


class Command(BaseCommand):
    name = "start"
    usage = "start <tournament_id>"
    description = "Start or Resume the tournament mode"

    def __init__(self) -> None:
        self.commands = Commands(package="app.commands.cmd_start")
        self.is_running = True

    def __quit(self):
        class Command(BaseCommand):
            name = "quit"
            usage = "quit"
            description = "quit the tournament mode"
            reload = False

            def run(_, context: typings.Context, **kwargs):
                self.is_running = False

        return Command()

    def _check_rounds(self, tournament):
        state = tournament.state

        try:
            tournament.round_instances[state.current_round]
        except IndexError:
            generated_round = tournament.generate_round()
            tournament.round_instances.append(generated_round)
            return tournament.save()
        return tournament

    def _check_commands(self, tournament):
        # Hide & unhide command based on state
        curr_round = tournament.state.current_round + 1

        disable_previous = False if curr_round > 1 else True
        self.commands.cache["previous"].is_disabled = disable_previous

        disable_next = True if curr_round == tournament.rounds else False
        self.commands.cache["next"].is_disabled = disable_next

        disable_next = True if len(tournament.round_instances) == tournament.rounds else False
        self.commands.cache["end"].is_disabled = disable_next

        enable_commit = False if tournament.state.is_ongoing else True
        self.commands.cache["commit"].is_disabled = enable_commit

    def run(self, context: typings.Context, args: list):
        context = context.copy()  # i don't want to modify the 'main' context
        self.commands.cache["quit"] = self.__quit()

        tournament_view = context["views"]["tournament"]
        tournament_model = context["models"]["Tournament"]

        tournament_id = self.pop_arg(args)
        tournament = tournament_model.find_one(tournament_id)

        if not tournament:
            raise errors.GenericError(f"Tournament with the id [{tournament_id}] doesn't exist")

        tournament = self._check_rounds(tournament)

        commands = self.commands.cache.values()
        self._check_commands(tournament)

        tournament_view.render_selected_tournament(tournament, commands)

        while self.is_running:
            try:
                input_content = input("-> : ").strip()
                args = input_content.split(" ")

                command_name = args.pop(0)
                self.commands.execute(command_name, args=args, context=context, tournament=tournament)
                tournament = tournament.save()

            except Exception as e:
                if not hasattr(e, "custom"):
                    errors.GenericError(e)

            if not self.is_running:
                # Its not an error, but its a way out
                raise errors.GenericError("Tournament Mode has been closed", title="Note")

            tournament = self._check_rounds(tournament)
            self._check_commands(tournament)
            tournament_view.render_selected_tournament(tournament, commands)
