"""
Pyety: Engine Console
"""

import cmd
import os

class Console(cmd.Cmd):
    """The Pyety console class implements a simple interactive interface."""

    def __init__(self, prompt="[Pyety]", logger=None):
        super().__init__()
        self.prompt = prompt + " "
        self.logger = logger

    def cmdloop(self, intro=None):
        """Override base cmdloop to better customize intro text."""
        if intro is None:
            self.intro = "Welcome to Pyety!" + os.linesep
        super().cmdloop(intro)

    def do_quit(self, save=False):
        """Exits the console interface."""
        saved = None
        while saved is None:
            if save == "y" or save == "Y":
                saved = True
            elif save == "n" or save == "N":
                saved = False
            else:
                print("Do you wish to save your game? (y/n)", end=" ")
                save = input()
        return True

    def do_start(self, args):
        """Start a new game."""
        pass
