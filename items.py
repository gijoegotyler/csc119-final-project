# CSC119-680
# Tyler Wright
# 2/9/2022

import math
# import libraries
import random
from typing import Optional


# define Item Base Class
class Item:
    # def basic init func
    def __init__(self, name: str):
        # give every item a name
        self.name = name
        # by default have items have no action
        self.action: Optional[str] = None


# make sword item
class Sword(Item):
    # append init to include power and durability stats
    def __init__(self, name: str, power: int, durability: int):
        Item.__init__(self, name)
        self.action = "Attack"
        self.power = power
        self.durability = durability

    def damage_item(self):
        damage = random.randrange(1, math.ceil(self.power / 5) + 2)
        self.durability -= damage

    def check_durabiliy(self):
        if self.durability <= 0:
            return "Broken"
        return ""


class Food(Item):
    # append init to include healing
    def __init__(self, name: str, healing: int):
        Item.__init__(self, name)
        self.action = "Eat"
        self.healing = healing
