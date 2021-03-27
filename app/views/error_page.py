from .abc import BaseView


class ErrorView(BaseView):
    def generic_error(self, message, centered=False):
        """Generic error, this will only have a message and a title to display"""
        self.body = []  # Reset the body to avoid duplicates

        message = self.center_item(message, char=" ") if centered else message

        self.set_title("Error Occured")
        self.add_body(message)

        self.set_footer("-")
        self.render_view()

        ## Waiter
        input(self.center_item("press enter to continue"))
