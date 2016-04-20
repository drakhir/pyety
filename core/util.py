"""
Pyety: Core Utilities
"""

import logging
import sys

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4

def get_logger(logger_name, loglevel=INFO, logfile='', logfmt='%(name)s - %(asctime)s - %(levelname)s - %(message)s'):
    """
    Set up logging. Default loglevel is INFO.
    Output is sent to stdout by default, or file of choice. Passing NoneType to logfile sets NullHandler.
    """
    logger = logging.getLogger(logger_name)
    if loglevel == DEBUG:
        logger.setLevel(logging.DEBUG)
    elif loglevel == INFO:
        logger.setLevel(logging.INFO)
    elif loglevel == WARNING:
        logger.setLevel(logging.WARNING)
    elif loglevel == ERROR:
        logger.setLevel(logging.ERROR)
    elif loglevel == CRITICAL:
        logger.setLevel(logging.CRITICAL)
    else:  # Throw error if loglevel is undefined.
        raise NotImplementedError
    formatter = logging.Formatter(logfmt, datefmt='%Y-%m-%d %H:%M:%S')
    if logfile:
        handler = logging.FileHandler(logfile)
    elif logfile is None:
        handler = logging.NullHandler()
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
