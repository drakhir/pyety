# -*- coding: utf-8 -*-

"""
Cell

The cell module creates a complex cell object capable of tracking numerous properties on the fly.
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


class Cell(object):
    """
    The cell class creates a more complex cell with the ability to calculate many different properties on the fly.
    Tested cell shapes include:
    Square/Cube - Length of one side is needed to calculate area and volume.
    Hexagon/Hexagonal prism - Length of one side needed to calculate area.  Height needed to calculate volume.
    """

    __slots__ = ['area', 'formula', 'height', 'icon', 'length', 'max_objs', 'measurements', 'shape', 'sides',
                 'volume', 'width']

    def __init__(self, shape, sides, max_objs=-1):
        try:
            self.shape = str(shape)
            self.sides = int(sides)
            self.max_objs = int(max_objs)
            self.icon = ""
            self.formula = {}
        except ValueError as err:
            logger.error("Error initializing grid cell.")
            raise ValueError(err)

    @property
    def area(self):
        return self._calculate('area')

    @property
    def height(self):
        return self._calculate('height')

    @property
    def length(self):
        return self._calculate('length')

    @property
    def width(self):
        return self._calculate('width')

    @property
    def volume(self):
        return self._calculate('volume')

    def _calculate(self, formula_type):
        """Calculate measurements."""
        try:
            kwargs = {}
            for m in self.formula[formula_type][0]:
                kwargs[m] = self.measurements[m]
            value = self.formula[formula_type][1](**kwargs)
        except (KeyError, NameError):
            logger.warning("No formula to calculate %s has been defined." % formula_type)
            value = None
        except IndexError:
            logger.error("Unable to calculate cell %s." % formula_type)
            logger.warning("Required measurements are %s. Currently measurements %s are set."
                         % (str(self.formula[formula_type][0]), str(tuple(self.measurements.keys()))))
            value = None
        return value

    def setFormula(self, **kwargs):
        """
        Set formulas for various measurements.  Currently, the supported measurements are area, height,
        length, width, and volume.
        """
        for k, v in list(kwargs.items()):
            self.formula[k] = v

    def setIcon(self, icon):
        """Set a default printable icon when the cell is empty."""
        self.icon = str(icon)

    def setMeasurements(self, **kwargs):
        """Sets the size for each necessary measurement of the cell shape."""
        self.measurements = {}
        try:
            for k, v in list(kwargs.items()):
                self.measurements[k] = int(v)
            if len(self.measurements) > 0:
                return True
            else:
                return False
        except ValueError:
            logger.error("Unable to set cell measurements.")
            return False
