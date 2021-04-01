from .abc import BaseView


class ErrorView(BaseView):
    def generic_error(self, message, centered=True):
        """Generic error, this will only have a message and a title to display"""
        self.body = []  # Reset the body to avoid duplicates

        # handle multilines
        message = message.split("\n")
        sanitized = []

        if centered:
            for line in message:
                line = self.center_item(line, char=" ")
                sanitized.append(line)

        message = "\n".join(sanitized)

        self.set_title("Error Occured")
        self.add_body(message)

        self.set_footer("-")
        self.render_view()

        ## Waiter
        input(self.center_item("press enter to continue"))

    def missing_value(self, missing_value, randomized=False):
        self.body = []  # Reset the body to avoid duplicates
        self.set_title("Missing Value")

        self.add_body(f"Missing value for : {self.colorize('warning', missing_value)}")

        if randomized:
            self.add_body("value has been randomized.")

        self.set_footer("-")
        self.render_view()

        ## Waiter
        input(self.center_item("press enter to continue"))