#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pyety: RPG Engine

Main script
"""

import os

import core.util
import ui.console as uic

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
log_dir = base_dir + os.sep + "log"
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
logger = core.util.get_logger("Pyety")

c = uic.Console()
c.cmdloop()
