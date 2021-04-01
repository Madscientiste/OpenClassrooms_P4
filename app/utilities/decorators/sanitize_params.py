def sanitize_params(func):
    def wrapper(self, args):
        action = args.pop(0) if len(args) else []

        if action:
            func(self, action, args)
        else:
            return self.context["main_view"].display_actions(actions=self.sub_commands)

    return wrapper