# -*- coding: utf-8 -*-

"""
Character

The Character module defines ways to import data from storage mechanisms such as a file or database then parse and
transport that data to other objects.  It also retrieves data from other objects and passes it back to the storage
mechanisms.
"""

from ..framework.asset import BaseAsset


class Character(BaseAsset):
    pass


class Player(Character):
    pass


class NonPlayer(Character):
    pass
