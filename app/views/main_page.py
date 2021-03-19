import os

from texttable import Texttable

from .abc import BaseView


class MainView(BaseView):
    def __init__(self, current_cmd) -> None:
        self.current_cmd = current_cmd

    def __show_example(self):
        self.add_body(" ")
        self.add_body(f" Example ".center(self.SCREEN_WIDTH, "-"))
        self.add_body(f" {self.current_cmd} <action> ".center(self.SCREEN_WIDTH, "-"))

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

    def display_actions(self, actions):
        """Display the available actions for a command"""
        self.body = []  # Reset the body to avoid duplicates

        text_table = Texttable()
        headers = ["Action Name", " ----- ", "Description"]

        rows = []
        middleRow = ""

        print("Action not found, or missing, here what you can do:")
        for action in actions.keys():
            action_desc = actions[action].__doc__
            rows.append([action, middleRow, action_desc])

        text_table.add_rows([headers, *rows])

        table = text_table.draw()
        table = self.center_table(table)

        self.set_title("Available Actions")
        self.add_body(table)

        self.__show_example()

        self.render_view()