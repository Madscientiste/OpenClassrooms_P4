from .base import BaseCommand

from app.controllers import Commands
from app.utilities import typings, errors

from app.models import database


class Command(BaseCommand):
    name = "start"
    usage = "start <tournament_id>"
    description = "Start the tournament mode"

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

    def _check_rounds(self, tournament, state):
        try:
            tournament.round_instances[state.current_round]
        except IndexError:
            generated_round = tournament.generate_round(state)
            tournament.round_instances.append(generated_round)
            return tournament.save()
        return tournament

    def _check_commands(self, state, tournament):
        # Hide & unhide command based on state
        curr_round = state.current_round + 1
        if curr_round == 1:
            self.commands.cache["previous"].is_disabled = True
        if curr_round > 1:
            self.commands.cache["previous"].is_disabled = False
        if curr_round == tournament.rounds:
            self.commands.cache["next"].is_disabled = True
            self.commands.cache["end"].is_hidden = False
        if curr_round < tournament.rounds:
            self.commands.cache["next"].is_disabled = False

    def run(self, context: typings.Context, args: list):
        context = context.copy()  # i don't want to modify the 'main' context
        self.commands.cache["quit"] = self.__quit()

        tournament_view = context["views"]["tournament"]
        tournament_model = context["models"]["Tournament"]

        tournament_id = self.pop_arg(args)

        # -------------------------------------------------------
        # Load the state & Checking if everything is correct
        # -------------------------------------------------------
        tournament = tournament_model.find_one(tournament_id)

        if not tournament:
            raise errors.GenericError(f"The id [{id}] wasn't found in database")

        state = database.State.find_one(tournament_id)

        if not state:
            state = database.State(current_round=0, is_ongoing=True).save(doc_id=tournament.id)

        # -------------------------------------------------------
        # Start the initialization of the tournament and generate the matches
        # -------------------------------------------------------

        tournament = self._check_rounds(tournament, state)

        # -------------------------------------------------------
        # Render
        # -------------------------------------------------------
        commands = self.commands.cache.values()
        self._check_commands(state, tournament)

        tournament_view.render_selected_tournament(tournament, state, commands)

        while self.is_running:
            try:
                input_content = input("-> : ").strip()
                args = input_content.split(" ")

                command_name = args.pop(0)
                self.commands.execute(command_name, args=args, context=context, tournament=tournament, state=state)
                tournament = tournament.save()

            except Exception as e:
                if not hasattr(e, "custom"):
                    errors.GenericError(e)

            if not self.is_running:
                # Its not an error, but its a way out
                raise errors.GenericError("Tournament Mode has been closed", title="Note")

            tournament = self._check_rounds(tournament, state)
            self._check_commands(state, tournament)
            tournament_view.render_selected_tournament(tournament, state, commands)
