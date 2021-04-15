from .abc import BaseSubCommand


class DeleteTournament(BaseSubCommand):
    name = "delete"
    usage = "tournament delete <tournament_id>"
    description = "delete a tournament"

    def __init__(self, context) -> None:
        super().__init__(context)

    def execute(self):
        pass