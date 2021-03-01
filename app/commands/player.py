from .cmd_player import create, update, delete, find

from .abc import BaseCommand


class PlayerCommand(BaseCommand):
    name = "player"

    sub_commands = {}
    sub_commands["create"] = create
    sub_commands["update"] = update
    sub_commands["delete"] = delete
    sub_commands["find"] = find

    # sub_commands = [create, update, delete, find]
    
    def execute(self, args):
        action = args.pop(0)

        self.execute_sub("create")
        # print("ayaya", action, self.sub_commands)
