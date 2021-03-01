from .player import create, update, delete, find

from .abc import BaseCommand


class TournamentCommand(BaseCommand):
    name = "tournament"

 