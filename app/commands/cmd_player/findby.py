from .abc import BaseSubCommand


class FindPlayer(BaseSubCommand):
    name = "findby"
    usage = "findby <action> <value>"
    description = "Find a Player by ID, Rank or first_name."

    def __init__(self, context) -> None:
        super().__init__(context)

        self.actions = {
            "*": self.find_all,
            "id": self.findby_id,
            "name": self.findby_name,
            "rank": self.findby_rank,
        }

    def execute(self, args):
        action = args.pop(0) if len(args) else None
        data = args.pop(0) if len(args) else None

        command = self.actions.get(action)

        if not command:
            # return self.main_veiw.display_actions(actions=self.actions)
            if action is not None:
                self.error_view.generic_error(f"Action [{action}] in [{self.name}] doesn't exist")

            self.main_view.display_actions(self.actions, is_class=False)
            return

        error = command(data)

        if error:
            self.error_view.generic_error(message=error)
            self.main_view.display_actions(self.actions, is_class=False)

    def find_all(self, data):
        """Find all the players that has been registred"""
        player_list = self.player_model.find_many(None, None)

        if not player_list:
            return "No players found"

        self.player_view.render_multiple_players(player_list, "Registred Player(s)")

    def findby_id(self, player_id):
        """Find one player by its Id"""

        if not player_id or not player_id.isdigit():
            return "id must be a number"

        found_player = self.player_model.find_one(id=int(player_id))

        if not found_player:
            return f"player id [{player_id}] not found"

        self.player_view.render_single_player(found_player, "Found Player")

    def findby_name(self, player_name):
        """Find many player by name (last name)"""
        found_players = self.player_model.find_many("last_name", player_name)

        if not found_players:
            return f"No players with name of [{player_name}] has been found"

        self.player_view.render_multiple_players(found_players, "Found Player(s)")

    def findby_rank(self, player_rank):
        """Find many players by rank"""

        if not player_rank or not player_rank.isdigit():
            return "rank must be a number"

        found_players = self.player_model.find_many("rank", player_rank)

        if not found_players:
            return f"player with [{player_rank}] rank not found"

        self.player_view.render_multiple_players(found_players, "Found Player(s)")