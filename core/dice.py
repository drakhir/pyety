# -*- coding: utf-8 -*-

"""
Pyety: Dice
"""

import random
from os import linesep

class Dice(object):
    """Simulate a dice roll"""

    def __init__(self):
        try:  # Initialize random seed
            self._r = random.SystemRandom()
        except NotImplementedError:  # Use the default randomization if no random number generator available
            pass
        # Initialize the dice roll history sequence
        self.history = []
        self.sides = []
        self.roll_mods = []

    def __len__(self):
        return len(self.history)

    def __str__(self):
        strrls = ""
        for n in range(len(self.history)):
            strrls = strrls + str(self.total(n - 1)) + linesep
        return strrls.rstrip()

    @property
    def rolls(self):
        if not self.history:  # The roll history is empty.
            all_rolls = []
        else:
            all_rolls = self.history
        return all_rolls

    @property
    def last(self):
        try:
            roll = self.history[-1]
        except IndexError:  # No last roll data found.
            roll = []
        return roll

    def discard(self, num, index=-1, reverse=False):
        dice = self.getRoll(index)
        dice.sort()
        if reverse:
            dice.reverse()
        dice = dice[num:]
        self.historyEdit(index, dice)
        return dice

    def getRoll(self, index):
        try:
            roll = self.history[index]
        except IndexError:  # Dice roll history index out of range.
            roll = []
        return roll

    def historyAppend(self, dice):
        self.history.append(dice)

    def historyEdit(self, index, dice):
        self.history[index] = dice

    def historyClear(self):
        self.history.clear()
        self.sides.clear()

    def reroll(self, index=-1, alg=lambda d: d < 2):
        dice = self.getRoll(index)
        new_dice = []
        history_offset = 0
        for die in dice:
            while alg(die):
                die = self.roll(self.sides[index], 1)
                die = die[0]
                if die and index < 0:
                    history_offset -= 1
            new_dice.append(die)
        index = index + history_offset
        self.historyEdit(index, new_dice)
        return new_dice

    def roll(self, sides, total_dice, modifier=0):
        self.sides.append(sides)
        self.roll_mods.append(modifier)
        try:
            dice = [self._r.randint(1, sides) for d in range(total_dice)]
            if dice:
                self.historyAppend(dice)
                dice = list(dice)
                dice.append(modifier)
        except (ValueError, TypeError):  # Dice roll failed due to invalid data.
            dice = []
        return dice

    def total(self, index=-1):
        try:
            value = sum(self.history[index]) + self.roll_mods[index]
        except IndexError:  # Roll history index out of range.
            value = 0
        return value
