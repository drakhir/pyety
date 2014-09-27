#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pyety RPG engine main script
"""

import sys
import logging

sys.path.append('/home/jason/src/projects/pyety')  # For testing purposes set local Python path.

logging.basicConfig(
                    level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="./log/pyety.log"
                    )
logger = logging.getLogger("Pyety")

from .ui import console

console.Console().cmdloop()
