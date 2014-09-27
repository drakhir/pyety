# -*- coding: utf-8 -*-

"""
This script contains a series of generic utility functions.
"""

import logging
import os.path
import sqlite3
from xml.dom import minidom
import xml.parsers.expat

logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                    )
logger = logging.getLogger(__name__)


def load(file_name):
    if os.path.isfile(file_name) and os.path.basename(file_name).endswith(".xml"):
        try:  # Try loading game asset data from XML file.
            xmlobj = minidom.parse(file_name)
        except xml.parsers.expat.ExpatError as err:
            logger.error("Unable to parse XML in %s." % file_name)
            info = {}
    elif os.path.isfile(file_name) and os.path.basename(file_name).endswith(".db"):
        db = sqlite3.connect(file_name)  # Load game asset data from sqlite3 database.
    else:
        logger.error("Unable to load game data from %s." % file_name)
        info = {}
    return info


def save(file_name):
    pass
