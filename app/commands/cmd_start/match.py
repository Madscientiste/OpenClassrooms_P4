from app.commands.base import BaseCommand
from app.utilities import typings, errors
from app.models import other, database


class Command(BaseCommand):
    name = "match"
    usage = "match <match_id>"
    description = "Select a match to update the score"

    def run(self, context: typings.Context, tournament: database.Tournament, args: list):
        round: other.Round = tournament.round_instances[tournament.state.current_round]
        tournament_view = context["views"]["tournament"]

        match_id = self.pop_arg(args)

        if not match_id:
            raise errors.GenericError("No <Match ID> given")
        if not match_id.isdigit():
            raise errors.GenericError("<Match ID> must be a number")

        try:
            match = round.get_match(int(match_id) - 1)
        except IndexError:
            raise errors.GenericError("Match ID doesn't exist")

        while True:
            tournament_view.render_match(match)
            whitelist = ["a", "b", "c", "d"]

            input_content = input("-> : ").strip()
            args = input_content.split(" ")
            command_name = args.pop(0)

            if command_name in whitelist:
                if command_name == "a":
                    match.settle_score(match.player1)
                    match.player1.points = 1
                    match.player2.points = 0

                elif command_name == "b":
                    match.settle_score(match.player2)
                    match.player2.points = 1
                    match.player1.points = 0

                elif command_name == "c":
                    match.player1.points = 0.5
                    match.player2.points = 0.5
                    match.settle_score("TIE")
                break  # i don"t need to add the command D
            else:
                continue
