import os

from texttable import Texttable

from .abc import BaseView


class ErrorView(BaseView):
    def __init__(self, current_cmd) -> None:
        self.current_cmd = current_cmd

    def missing_action(self, actions):
        """Display the available actions for a command"""
        self.body = []  # Reset the body to avoid duplicates

        text_table = Texttable()
        headers = ["Action Name", " ----- ", "Description"]
        header_size = len(headers)

        rows = []
        middleRow = ""

        print("Action not found, or missing, here what you can do:")
        for action in actions.keys():
            action_desc = actions[action].__doc__
            rows.append([action, middleRow, action_desc])

        text_table.add_rows([headers, *rows])
        table = text_table.draw()

        self.set_title("Missing Action")
        self.add_body(table)

        # return table
        self.add_body("")
        self.add_body("Example:")
        self.add_body(f"{self.current_cmd} <action>")

        self.set_footer(" Waiting Input ")
        self.render_view()

    def generic_error(self, message):
        """Generic error, this will only have a message and a title to display"""

        self.body = []  # Reset the body to avoid duplicates
        self.set_title("Error Occured")
        self.add_body(message)
        self.set_footer("-")
        self.render_view()

        ## Waiter
        input("press enter to continue")
