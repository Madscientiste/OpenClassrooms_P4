from .base import BaseCommand
from app.utilities import typings


class Command(BaseCommand):
    name = "tournament"
    usage = "tournament <command>"
    description = "tournament related command"

    def run(self, context: typings.Context, args: list):
        print("runninngingng")
