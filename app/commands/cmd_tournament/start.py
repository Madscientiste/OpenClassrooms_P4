from .abc import BaseSubCommand


class StartTournament(BaseSubCommand):
    name = "start"
    usage = "tournament start <tournament_id>"
    description = "Start/Resume a tournament"

    def __init__(self, context) -> None:
        super().__init__(context)
        self.isRunning = True
        self.current_round = 1


    def _generate_pair(self, players, current_round):
        players = sorted(players, key=lambda player: int(player["rank"]), reverse=True)
        
        matches = {}
        match_id = lambda: str(len(matches.keys()) + 1)
        
        locked = []
        pairing = []

        if current_round == 1:
            # split the array in half
            length = len(players)
            middle_index = length // 2

            superieur = players[:middle_index]
            inferieur = players[middle_index:]

            # Pair the players together
            for player1, player2 in zip(superieur, inferieur):
                player1["history"].append(player2["id"])
                player2["history"].append(player1["id"])

                matches[match_id()] = [player1, player2]
        else:
            for p1_index, current_player in enumerate(players):
                if p1_index not in locked:
                    locked.append(p1_index)
                
                    for p2_index, next_player in enumerate(players):
                        played_together = next_player.doc_id in current_player["history"]

                        if p2_index in locked or played_together:
                            continue

                        locked.append(p2_index)
                        matches[match_id()] = [current_player, next_player]
                        
                        current_player["history"].append(current_player.doc_id)
                        next_player["history"].append(next_player.doc_id)

        return matches

    def _cmd_next_round(self):
        self.current_round += 1

    def _cmd_quit(self, args, matches):
        """Quit the tournament mode"""
        self.isRunning = False

    def _cmd_match(self, args, matches):
        """Select a match using its ID"""
        match_id = args.pop(0) if len(args) else None

        if not match_id:
            return "No match ID has been given"

        if not match_id.isdigit():
            return "Match ID must be a number"

        match = matches.get(match_id)

        if not match:
            return f"ID [{match_id}] doesn't belong to a match"

        whitelist = ["1", "2", "*", "-"]

        while True:
            self.tournament_view.render_match(match)
            result = input("-> : ")

            if result not in whitelist:
                self.error_view.generic_error(message="Wrong input")
                continue

            if result == "1":
                match[0]["points"] = 1
                match[1]["points"] = 0
                break

            if result == "2":
                match[0]["points"] = 0
                match[1]["points"] = 1
                break

            if result == "*":
                match[0]["points"] = 0.5
                match[1]["points"] = 0.5
                break

            if result == "-":
                break

    def execute(self, args):
        tournament_id = args.pop(0) if len(args) else None

        if not tournament_id:
            self.error_view.generic_error("No tournament id given")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        if not tournament_id.isdigit():
            self.error_view.generic_error(message="id must be a number")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        tournament = self.tournament_model.find_one(tournament_id)

        if not tournament:
            self.error_view.generic_error(message="No tournament found")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        players = tournament["players"]

        commands = {
            "match": self._cmd_match,
            "quit": self._cmd_quit,
        }

        while self.isRunning:
            matches = self._generate_pair(players, self.current_round)
            
            self.tournament_view.render_tournament(tournament, matches, commands=commands)

            input_content = input("-> : ").strip()
            args = input_content.split(" ")

            cmd_name = args.pop(0)

            if not cmd_name:
                self.error_view.generic_error(message="No input given", centered=True)
                continue

            command = commands.get(cmd_name)

            if not command:
                self.error_view.generic_error(message="No command found", centered=True)
                continue

            error = command(args, matches)

            if error:
                self.error_view.generic_error(message=error)
                continue

            # Saving the changes after each command
            self.tournament_model.update_one(tournament)

        if not self.isRunning:
            self.main_view.display_actions(actions=self.sub_commands)
