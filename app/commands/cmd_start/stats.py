from app.commands.base import BaseCommand
from app.models import database


class Command(BaseCommand):
    name = "report"
    usage = "report <sort_by> <key>"
    description = "Show the report of the current Tournament"

    def run(self, tournament: database.Tournament, *args, **kwargs):
        pass
