from .base import BaseView


class View(BaseView):
    """MainView"""

    def render_main_page(self, commands: list, tournaments: list, states: list):
        self.set_title("Main Application")

        self.add_body("Ongoing Tournaments")
        self.add_body("------------------")
        self.add_body("")

        for index, tournament in enumerate(tournaments):
            index += 1
            state = [x for x in states if x.id == tournament.id].pop(0)

            if not state.is_ongoing:
                continue

            self.add_body(f"=====> Tournament {index} of {len(tournaments)}")
            self.show_tournament(tournament)
            self.add_body(" ")

        self.add_body(self.center_item("-", "-", no_space=True))

        self.add_body("")

        self.add_body("Available Commands")
        self.add_body("------------------")
        self.add_body("")

        self.show_commands(commands)

        self.add_body("")
        self.add_body("To Exit the application do [CTRL + C] at anytime")
        self.add_body("")
        self.render_view()

    def render_available_commands(self, commands: list):
        self.set_title("Available Commands")
        self.show_commands(commands)
        self.render_view()

    def application_quit(self):
        self.set_title("Main Application")
        self.add_body(self.center_item("Application Terminated"))
        self.set_footer("-------")
        self.render_view()
