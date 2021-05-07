from app.commands.base import BaseCommand
from app.utilities import typings, errors
from app.models import other, database


class Command(BaseCommand):
    name = "previous"
    usage = "previous"
    description = "Go to the previous round"

    def run(self, context: typings.Context, tournament: database.Tournament, args: list, state: database.State):
        if state.current_round == 0:
            return

        state.current_round -= 1
        state.save()