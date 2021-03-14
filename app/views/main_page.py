import os

from texttable import Texttable

from .abc import BaseView


class MainView(BaseView):
    def render_main_page(self, commands):
        self.body = []

        self.set_title("Main Application")
        self.add_body("Available Commands")
        self.add_body("------------------")
        self.add_body("")

        for command in commands:
            name = command.name
            description = command.description
            usage = command.usage

            if not command.is_hidden:
                self.add_body(f"-> {name} ")
                self.add_body(f"---- Description : {description} ")
                self.add_body(f"---- Usage: {usage} ")
                self.add_body(" ")

        self.add_body("".center(self.SCREEN_WIDTH, "-"))

        self.add_body("")
        self.add_body("Ongoing Tournaments")
        self.add_body("-------------------")
        self.add_body("")

        self.add_body("[id] -> Tournament Name")
        self.add_body("------- location")
        self.add_body("------- date")
        self.add_body("------- turns")
        self.add_body("------- players")
        self.add_body("------- players")
        self.add_body("------- time_control")
        self.add_body("------- description")

        self.set_footer(" Waiting Input ")
        self.render_view()