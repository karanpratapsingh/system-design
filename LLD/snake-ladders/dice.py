import random

class Dice():

    def __init__(self, sides) -> None:
        self.sides = sides

    def get_value(self):
        return random.randint(1, self.sides)