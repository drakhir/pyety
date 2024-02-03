#!/usr/bin/env python
# pylint: disable=C0103,C0301

"""
Pyety: RPG Engine

Main script
"""

import os

import core.util
import ui.console as uic

def conf_logger(logger_name, log_dir=None):
    """Configure logging"""
    if not log_dir:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        log_dir = base_dir + os.sep + "log"
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    logger = core.util.get_logger(logger_name)
    return logger

def run_console():
    """Run console UI"""
    log = conf_logger("pyety.console")
    con = uic.Console(logger=log)
    con.cmdloop()

def run_gui():
    """Run graphical UI"""
    pass

def main():
    """Main function"""
    run_console()

if __name__ == "__main__":
    main()
