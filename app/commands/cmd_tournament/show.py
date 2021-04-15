import random

from .abc import BaseSubCommand


class ShowTournament(BaseSubCommand):
    name = "show"
    usage = "tournament show"
    description = "Show all tournaments"

    def __init__(self, context) -> None:
        super().__init__(context)

    def execute(self, args):
        """Execution of the current command"""
        tournaments = self.tournament_model.find_all()

        if not tournaments:
            self.error_view.generic_error("No tournaments found")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        self.tournament_view.render_all_tournaments(tournaments, "Current Tournaments")
