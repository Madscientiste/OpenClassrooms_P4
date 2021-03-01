class BaseCommand:
    name = None
    sub_commands = {}

    def __init__(self) -> None:
        pass

    def sanitize_args(self, args) -> None:
        pass

    def execute(self, args):
        pass

    def execute_sub(self, sub_cmd):
        cmd_list = self.sub_commands
        
        print(cmd_list)
        pass
