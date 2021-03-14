def sanitize_params(func):
    def wrapper(self, args):
        action = args.pop(0) if len(args) else []

        if not action:
            return self.context["error_view"].missing_action(actions=self.sub_commands)

        func(self, action, args)

    return wrapper