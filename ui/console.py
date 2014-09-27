# -*- coding: utf-8 -*-

"""
Pyety RPG engine console
"""

import logging
import cmd

log_name = "Pyety[" + __name__ + "]"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(log_name)


class Console(cmd.Cmd):
    """The Pyety console class implements a simple interactive interface."""

    prompt = "[Pyety] "

    def cmdloop(self, intro=""):
        """Override base cmdloop to better customize intro text."""
        logger.debug("Launching Pyety console.")
        if not intro:
            intro = "Welcome to Pyety!" + "\n"
        super().cmdloop(intro)

    def do_quit(self, save=None):
        """Exits the console interface."""
        logger.debug("Exiting application...")
        saved = None
        while saved is None:
            if save == "y" or save == "Y" or save == "save":
                saved = True
                logger.info("Saving game.")
            elif save == "n" or save == "N" or save == "now":
                saved = False
                logger.info("Exiting without saving.")
            else:
                print("Do you wish to save your game? (y/n) ", end="")
                save = input()
        return True

    def do_start(self, args):
        """Start a new game."""
        logger.debug("Beginning a new game.")
