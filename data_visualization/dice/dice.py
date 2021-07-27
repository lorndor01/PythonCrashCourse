from random import randint

class Dice:
    """A class to represent a single dice."""

    def __init__(self, num_sides=6):
        """Assume a six-sided dice."""
        self.num_sides = num_sides

    def roll(self):
        """Return a random number between 1 and the number of sides"""
        return randint(1, self.num_sides)