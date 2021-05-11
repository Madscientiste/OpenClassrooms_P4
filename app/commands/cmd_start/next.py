from app.commands.base import BaseCommand
from app.utilities import errors
from app.models import database


class Command(BaseCommand):
    name = "next"
    usage = "next"
    description = "Go to the next round"

    def run(self, tournament: database.Tournament, *args, **kwargs):
        if tournament.state.current_round + 1 == tournament.rounds:
            return

        round = tournament.round_instances[tournament.state.current_round]

        # Can't go to the next round if the matches aren't completed
        if None in [x.winner for x in round.matches]:
            raise errors.GenericError("Can't go to the next round, some matches need to be completed first")

        if not round.end_date:
            round.end_round()

        tournament.state.current_round += 1

        # Testing if we can generate a new round
        if not len(tournament.generate_round().get_players()):
            tournament.state.is_ongoing = False
            tournament.state.current_round -= 1
            raise errors.GenericError("Cannot generate a new round, everyone played agaist each other !")
