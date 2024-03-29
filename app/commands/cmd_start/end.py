from app.commands.base import BaseCommand
from app.utilities import errors
from app.models import database


class Command(BaseCommand):
    name = "end"
    usage = "end"
    description = "Mark the tournament as ended"

    def run(self, tournament: database.Tournament, *args, **kwargs):
        if not tournament.state.is_ongoing:
            raise errors.GenericError("Tournament is already marked as done")

        round = tournament.round_instances[tournament.state.current_round]

        if None in [x.winner for x in round.matches]:
            raise errors.GenericError("Cannot end the tournament, some matches are not completed")

        if not round.end_date:
            round.end_round()

        tournament.state.is_ongoing = False

        raise errors.GenericError(
            "Tournament has been marked as finished, you can now quit the tournament mode",
            title="Note",
        )
