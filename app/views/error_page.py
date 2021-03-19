import os

from texttable import Texttable

from .abc import BaseView


class ErrorView(BaseView):
    def generic_error(self, message):
        """Generic error, this will only have a message and a title to display"""

        self.body = []  # Reset the body to avoid duplicates
        self.set_title("Error Occured")
        self.add_body(message)
        self.set_footer("-")
        self.render_view()

        ## Waiter
        input("press enter to continue")
