# CSC119-680
# Tyler Wright
# 2/9/2022

# import Player object for type hinting
from player import Player

# define Item Base Class
class Item:
    # def basic init func
    def __init__(self, name: str):
        # give every item a name
        self.name = name
        # by default have items have no action
        self.action = None

# make sword item
class Sword(Item):
    # append init to include power and durability stats
    def __init__(self, name: str, power: int, durability: int):
        Item.__init__(self, name)
        self.action = "Attack"
        self.power = power
        self.durability = durability
    
class Food(Item):
    # append init to include healing 
    def __init__(self, name: str, healing: int):
        Item.__init__(self, name)
        self.action = "Eat"
        self.healing = healing
    
    # set action function to heal passed player object 
    def Eat(self, player: Player):
        if player.hp + self.healing <= player.max_hp:
            player.hp += self.healing
        else:
            player.hp = player.max_hp