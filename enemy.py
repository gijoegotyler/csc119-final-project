# CSC119-680
# Tyler Wright
# 2/9/2022

# import libraries
from typing import Optional, Union


# define Enemy class
class Enemy:
    # def
    def __init__(self, name: str, health: int, power: int):
        self.name = name
        self.health = health
        self.power = power
