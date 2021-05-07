from .base import BaseView


class View(BaseView):
    """ErrorView
    All errors should be rendered with this view
    """

    def _with_traceback(self, error):
        if hasattr(error, "custom") or not hasattr(error, "__traceback__"):
            return
        
        self.add_body(" ")
        traceback = error.__traceback__

        self.add_body(self.center_item("-", "-", True))

        self.add_body("")
        self.add_body("Traceback")
        self.add_body("-------------------")
        self.add_body("")

        while traceback is not None:
            self.add_body(
                f"File : {traceback.tb_frame.f_code.co_filename}\n"
                f"-- Line : {traceback.tb_lineno}\n"
                f"-- In   : {traceback.tb_frame.f_code.co_name}\n"
            )
            traceback = traceback.tb_next

    def generic_error(self, error, title=None, centered=True):
        """Generic error, this will only have a message and a title to display"""
        self.reset_values()

        self.set_title("Error Occured" if not title else title)
        self.set_footer("Press enter to continue")

        message = self.center_item(error) if centered else error

        self.add_body(message)
        self._with_traceback(error)

        self.render_view(wait=True)

    def command_not_found(self, command_name, parent_command, commands):
        """Error for commands that wasn't found"""
        self.reset_values()

        self.set_title("Error Occured")
        self.set_footer("Press enter to continue")

        color_command_name = self.colorize("warning", f"[{command_name}]")
        color_parent_command = self.colorize("info", f"[{parent_command}]")

        with_parent = f" in {color_parent_command} " if parent_command else " "

        message = self.center_item(
            f"!!! The command {color_command_name} couldn't be found{with_parent}!!!", is_colored=True
        )

        self.add_body(message)
        self.add_body("")
        self.add_body(self.center_item(f"- List of available commands{with_parent}-", "-"))
        self.add_body(" ")

        for command in commands:
            for field in ["name", "usage", "description"]:
                self.add_body(f"-- {field} : {command.__getattribute__(field)}")

            self.add_body("-" * 50)
            self.add_body(" ")

        self.render_view(wait=True)
