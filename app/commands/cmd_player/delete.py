import random

from faker import Faker

from .abc import BaseSubCommand


class DeletePlayer(BaseSubCommand):
    name = "delete"
    usage = "player delete <player_id>"
    description = "Delete a player using an ID"

    def __init__(self, context) -> None:
        super().__init__(context)

    def execute(self, args):
        player_id = args.pop(0) if len(args) else None

        if not player_id or not player_id.isdigit():
            self.error_view.generic_error(message="id must be a number")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        pre_delete = self.player_model.find_one(id=int(player_id))
        deleted_players = self.player_model.delete_one(id=int(player_id))

        if not deleted_players:
            self.error_view.generic_error(message=f"player id [{player_id}] not found")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        if pre_delete.doc_id == deleted_players.pop(0):
            self.player_view.render_single_player(pre_delete, "Deleted Player")
        else:
            self.error_view.generic_error(message=f"Doesn't Match")
            self.main_view.display_actions(actions=self.sub_commands)
