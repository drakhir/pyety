# -*- coding: utf-8 -*-

"""
Location

Classes which allow object tracking across 2D or 3D space.
"""

import logging
from uuid import uuid4
from os import linesep

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
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


class Grid(object):
    """Tracks the location of objects on a grid."""

    __slots__ = ['area', 'cell', 'content', 'dimensions', 'height', 'idmap', 'layers', 'layer_size', 'length',
                 'locations', 'objs', 'scope', 'size', 'surface', 'volume', 'uid', 'width']

    def __init__(self, cellobj=None):
        self.uid = uuid4().hex
        self.cell = cellobj
        self.idmap = {}
        self.objs = {}
        self.locations = {}

    def __call__(self):
        print(self)

    def __str__(self):
        grid = self.printSurface()
        grid += self.printContent()
        return grid

    @property
    def area(self):
        """The total area of the grid."""
        try:
            area = self.cell.area * self.size[0]
        except (IndexError, TypeError):
            logger.error("Unable to calculate total area of grid %s." % self.uid)
            area = 0
        return area

    @property
    def dimensions(self):
        """The number of dimensions the grid exists in."""
        try:
            if self.scope[2] > 1:
                return 3
            else:
                return 2
        except IndexError:
            logger.error("Grid scope out of range.")
            return 0

    @property
    def layers(self):
        """Returns the number of grid layers."""
        return self.scope[2]

    @property
    def layer_size(self):
        """Returns the number of grid cells per layer."""
        return self.scope[0] * self.scope[1]

    @property
    def size(self):
        """Returns the total number of grid cells."""
        if self.layers > 1:
            return self.scope[0] * self.scope[1] * self.scope[2]
        else:
            return self.scope[0] * self.scope[1]

    @property
    def volume(self):
        """The total volume of the grid."""
        if self.layers > 1:
            try:
                volume = self.cell.volume * self.size[0]
            except (IndexError, TypeError):
                logger.error("Unable to calculate total volume of grid %s." % self.uid)
                volume = 0
            return volume
        else:
            return 0

    def clear(self):
        """Clear the grid of all content"""
        self.idmap = {}
        self.objs = {}
        self.locations = {}
        if self.cell:
            icon = self.cell.icon
        else:
            icon = ""
        self.surface = [[icon for i in range(self.size)] for o in range(self.scope[2])]
        self.content = [[[] for i in range(self.size)] for o in range(self.scope[2])]

    def create(self, x, y, z=1):
        """Create (or overwrite) a grid.  If z=1 then a two dimensional grid is created."""
        try:
            x = int(x)
            y = int(y)
            z = int(z)
            size = x * y
        except ValueError as exc:
            logger.error(exc)
            return False
        if x < 1 or y < 1 or z < 1 or size < 1:
            logger.error("Creation failed: Total grid size less than one.")
            return False
        else:
            if self.cell:
                icon = self.cell.icon
            else:
                icon = ""
            self.scope = (x, y, z)
            self.surface = [[icon for i in range(size)] for o in range(z)]
            self.content = [[[] for i in range(size)] for o in range(z)]
            logger.info("Successfully created a new grid with a size of %s by %s by %s." % (x, y, z))
            return True

    def getCell(self, location):
        """Get contents of a single grid cell.  Returns a tuple of (surface, content)."""
        index = self.index(location)
        try:
            bg = self.surface[index[0]][index[1]]
            fg = self.content[index[0]][index[1]]
            cell = (bg, fg)
        except (IndexError, TypeError):
            logger.error("Grid location is out of range.")
            cell = ()
        return cell

    def getCoordinates(self, name):
        """Get location of a game piece."""
        try:
            location = self.locations[name]
        except KeyError:
            logger.error("Object %s does not exist on grid." % name)
            location = None
        return location

    def printContent(self):
        """Returns a basic visual representation of a grid's content."""
        try:
            #test = self.content[0]
            grid = "\tGrid Content" + linesep
            for level in self.content:
                grid += linesep
                grid += "\tLevel " + str(level + 1) + ":" + linesep
                count = 0
                for cell in self.content[level]:
                    count += 1
                    if len(cell) == 1:
                        text = cell[0]
                    elif len(cell) > 1:
                        text = str(len(cell))
                    else:
                        text = "-"
                    grid += "\t" + text
                    if count % self.scope[1] == 0:
                        grid += linesep
        except (AttributeError, IndexError):
            grid = "The grid is empty."
        grid += linesep
        return grid

    def printSurface(self):
        """Returns a basic visual representation of a grid's surface."""
        try:
            #test = self.surface[0]
            grid = "\tGrid Surface" + linesep
            for level in self.surface:
                grid += linesep
                grid += "\tLevel " + str(level + 1) + ":" + linesep
                count = 0
                for cell in self.surface[level]:
                    count += 1
                    if not cell:
                        cell = "-"
                    grid += "\t" + cell
                    if count % self.scope[1] == 0:
                        grid += linesep
        except (AttributeError, IndexError):
            grid = "The grid's surface is blank."
        grid += linesep
        return grid

    def add(self, location, obj, name):
        """
        Add an object to a grid. If no Cell object is defined for this grid each
        cell may only hold a single object.
        """
        index = self.index(location)
        try:  # Make sure grid index is valid before continuing.
            cell = self.content[index[0]][index[1]]
        except (IndexError, TypeError):
            logger.error("Grid location is out of range.")
            return False
        if obj in list(self.objs.values()):
            logger.error("Game piece object %s already exists in grid." % obj)
            return False
        elif name in self.locations:
            logger.error("Game piece %s already exists." % name)
            return False
        else:
            in_cell = len(cell)
            if self.cell:
                if self.cell.volume:
                    pass
                elif self.cell.max_objs == 0 or self.cell.max_objs > in_cell:
                    pass
                else:
                    logger.error("Huh?")
                    return False
            else:
                if in_cell == 0:
                    self.content[index[0]][index[1]].append(obj)
                    location = [location, in_cell]
                    self.idmap[id(obj)] = name
                    self.locations[name] = location
                    self.objs[name] = obj
                    result = name
                else:
                    logger.error("Unable to add object to grid. Each cell may only hold a single object.")
                    return False
        logger.info("Successfully added object %s at location %s, %s, %s." %
                    (name, location[0], location[1], location[2]))
        return result

    def delete(self, name):
        """Remove an object from a grid."""
        try:
            location = self.locations[name]
            piece = self.objs[name]
        except KeyError:
            logger.error("Game piece %s does not exist." % name)
            return False
        try:
            index = self.index(location[0])
            del self.content[index][location[1]]
            for n in range(location[1], len(self.content[index])):
                opiece = self.content[index][n]
                oname = self.idmap[id(opiece)]
                self.locations[oname][1] -= 1
            del self.locations[name]
            del self.objs[name]
            del self.idmap[id(piece)]
            result = True
        except (IndexError, TypeError):
            logger.error("Grid location is out of range.")
            return False
        logger.info("Successfully deleted game piece %s." % name)
        return result

    def index(self, location):
        """Calculates list index of a grid cell. Mainly meant for internal use."""
        if location[0] > self.scope[0] or location[1] > self.scope[1] or location[2] > self.scope[2]:
            logger.error("Grid index out of range.")
            return ()
        try:
            index = (location[2] - 1, (location[0] - 1) * self.scope[1] + location[1] - 1)
        except (IndexError, TypeError):
            logger.error("Grid index out of range.")
            index = ()
        return index

    def move(self, name, location):
        """Move an existing object to a new location on a grid."""
        logger.info("Attempting to move object %s." % name)
        try:
            piece = self.objs[name]
        except KeyError:
            logger.error("Game piece %s does not exist." % name)
            return False
        new_index = self.index(location)
        try:  # Make sure grid index is valid before moving on.
            cell = self.content[new_index]
        except (IndexError, TypeError):
            logger.error("Grid location is out of range.")
            return False
        result = self.delete(name)
        if result:
            result = self.add(location, piece, name)
        if result:
            logger.info("Successfully moved object %s to location %s, %s on grid." % (name, location[0], location[1]))
            return result
        else:
            logger.error("Unable to move %s to location %s, %s." % (name, location[0], location[1]))
            return result

    def paint(self, location, piece):
        """
        Paint (add) an immovable object to a grid's surface. This could be useful for decorating
        the grid, such as for creating terrain or various other purposes.
        """
        index = self.index(location)
        try:
            self.surface[index] = piece
        except (IndexError, TypeError):
            logger.error("Grid location is out of range.")
            return False
        logger.info("Set a surface cell at location %s, %s." % (location[0], location[1]))
        return True
