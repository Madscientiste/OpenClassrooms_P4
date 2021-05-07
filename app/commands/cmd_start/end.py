from app.commands.base import BaseCommand
from app.utilities import typings, errors
from app.models import other, database


class Command(BaseCommand):
    name = "end"
    usage = "end"
    description = "End the tournament and update the players's rank"
    # Hide it, because they 'could' can end the tournament while they shouldn't
    is_hidden = True

    def run(self, context: typings.Context, tournament: database.Tournament, args: list, state: database.State):
        round = tournament.round_instances[state.current_round]

        if None in [x.winner for x in round.matches]:
            raise errors.GenericError("Cannot end the tournament, match not completed")

        if not round.end_date:
            round.end_round()

        state.is_ongoing = False
        state.save()