# -*- coding: utf-8 -*-

import logging

logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

import random
from os import urandom


class Dice(object):
    """Simulate a dice roll"""

    def __init__(self, num=random.randint(1, 256)):
        try:  # Initialize random seed
            random.seed(urandom(num))
        except NotImplementedError:  # Use the default randomization if no random number generator available
            logger.warning("System random number generator unavailable. Using defaults.")
            pass
        # Initialize the dice roll history chain
        self.roll_history = []
        self.sides = []

    def __len__(self):
        return len(self.roll_history)

    def __str__(self):
        return str(self.total)

    @property
    def all(self):
        if not self.roll_history:
            logger.warning("The roll history is empty.")
            return []
        else:
            return self.roll_history

    @property
    def last(self):
        try:
            return self.roll_history[-1]
        except IndexError:
            logger.warning("No last roll data found")
            return []

    @property
    def total(self):
        return sum(self.last)

    def tally(self, index):
        try:
            return sum(self.roll_history[index])
        except IndexError:
            logger.error("The dice roll_history index is out of range.")
            return []

    def rollHistoryAppend(self, dice):
        self.roll_history.append(dice)

    def rollHistoryEdit(self, index, dice):
        self.roll_history[index] = dice

    def rollHistoryClear(self):
        self.roll_history = []
        self.sides = []

    def discard(self, num, index=None, reverse=False):
        if index is None:
            dice = self.last
        else:
            dice = self.getRoll(index)
        dice.sort()
        if reverse:
            dice.reverse()
        dice = dice[num:]
        self.rollHistoryEdit(index, dice)
        return dice

    def getRoll(self, index):
        h = list(self.roll_history)
        if index >= 0:
            h.reverse()
        try:
            roll = h[index]
            return roll
        except IndexError:
            logger.error("The dice roll_history index is out of range.")
            return []

    def reroll(self, index=None, alg=None):
        if index is None:
            dice = self.last
            index = -1
        else:
            dice = self.getRoll(index)
        new_dice = []
        for die in dice:
            if alg is None:
                alg = lambda d: d < 2
            while alg(die):
                die = self.roll(self.sides[index], 1)
                die = die[0]
            new_dice.append(die)
        self.rollHistoryEdit(index, new_dice)
        return new_dice

    def roll(self, sides, total_dice):
        self.sides.append(sides)
        try:
            dice = [random.randint(1, sides) for d in range(total_dice)]
            if dice:
                self.rollHistoryAppend(dice)
            return dice
        except (ValueError, TypeError):
            logger.error("Dice roll failed due to invalid data.")
            return []
