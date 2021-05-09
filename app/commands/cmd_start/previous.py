from app.commands.base import BaseCommand
from app.models import database


class Command(BaseCommand):
    name = "previous"
    usage = "previous"
    description = "Go to the previous round"

    def run(self, tournament: database.Tournament, *args, **kwargs):
        if tournament.state.current_round > 0:
            tournament.state.current_round -= 1
