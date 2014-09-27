# -*- coding: utf-8 -*-

"""
Base Deity Asset

Defines all the basic functionality for deity game objects, but not specific
types of objects or what specific data those objects should contain.
"""

import logging
import uuid

logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                    )
logger = logging.getLogger(__name__)


def validate(asset, attribs=()):
    if "uuid" not in asset or not asset.uuid:
        return False
    if len(attribs) == 0:
        return True
    else:
        for attrib in attribs:
            if attrib not in asset:
                return False
        return True


class BaseAsset(object):
    """Base Deity asset class."""

    def __init__(self, required=(), data={}):
        self.required_attr = required
        self.uuid = uuid.uuid4().hex
        try:
            if data:
                for name, value in list(data.items()):
                    self.__setattr__(name, value)
        except AttributeError as err:
            raise AttributeError(err)

    def __str__(self):
        data = "Statistics for asset: " + str(self.uuid)
        for name, value in list(self.__dict__.items()):
            if name == "uuid":
                continue
            data += "\n" + name + ":\t\t\t" + str(value)
        return data

    def __getattr__(self, name):
        pass

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name in self.required_attr:
            raise AttributeError("Unable to delete attribute %s. The attribute is required." % name)
        else:
            object.__delattr__(self, name)

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        for name, value in list(self.__dict__.items()):
            yield (name, value)

    def __contains__(self, key):
        if key in self.__dict__:
            return True
        else:
            return False

    def __call__(self):
        print((self.__str__()))
