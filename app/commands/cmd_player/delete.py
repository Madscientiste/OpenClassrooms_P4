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

        deleted_player = self.player_model.delete_one(id=int(player_id))

        if not deleted_player:
            self.error_view.generic_error(message=f"player id [{player_id}] not found")
            self.main_view.display_actions(actions=self.sub_commands)
            return

        self.player_view.render_single_player(deleted_player, "Deleted Player")
