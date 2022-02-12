# CSC119-680
# Tyler Wright
# 2/9/2022

# import libraries
from typing import Optional, Union

# import Player object for type hinting
from player import Player
from items import *

# define Enemy class
class Enemy:
    # def
    def __init__(self, health: int, power: int, reward: Optional[Union[Item, Food, Sword]] = None):
        self.health = health
        self.power = power

    
    def Attack(self, player: Player):
        player.hp -= self.power
        player.check_hp()