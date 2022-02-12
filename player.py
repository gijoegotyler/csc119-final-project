# CSC119-680
# Tyler Wright
# 2/9/2022

# import libraries
import math
import sys

# import Player and Items object for type hinting
from items import Food

# define player class
class Player:
    # initialize player class
    def __init__(self):
        # set base skill values
        self.skills = {
            "Strength": 1,
            "Speed": 1,
            "Defense": 1,
            "Intelligence": 1,
            "Vitality": 1,
            "Magic": None,
            "Crafting": None,
        }

        # set base hp and max hp
        self.max_hp = self.skills["Vitality"] * 3
        self.hp = self.max_hp

        # generate empty inventory
        self.inventory = []

        # set base level and experience
        self.level = 1
        self.experience = 0

    def level_up(self):
        # let user know about level and increment level
        print("You leveled up!")
        self.level += 1

        # if level reached is 10 unlock magic / crafting
        if self.level == 10:
            print("You unlocked Magic and Crafting skills")
            self.skills["Magic"] = 1
            self.skills["Crafting"] = 1

        # loop through available skills and print them with index
        for i in range(len(self.skills)):
            skill = list(self.skills)[i]
            if self.skills[skill] is not None:
                print(f"{i}) {skill}")

        # get user input to decide which skill to improve and level it based on the user level
        selection = int(input("Which skill do you upgrade: "))
        self.skills[list(self.skills)[selection]] += self.level // 3 + 1

        # if the skill leveled was vitality apply its health bonuses
        if list(self.skills[selection]) == "Vitality":
            prev_max_hp = self.max_hp
            self.max_hp = self.skills["Vitality"] * 3
            self.hp += self.max_hp - prev_max_hp

    def check_level_up(self):
        # calculate required exp for level up
        req_exp = math.ceil(5 * (math.log(self.level) ** 1.5) + 10)

        # if the exp req is met remove the req exp and call level up code
        if self.experience >= req_exp:
            self.experience -= req_exp
            self.level_up()

    def check_hp(self):
        # ensure that if you run out of health you die and the game ends and you dont go over max hp
        if self.hp <= 0:
            print("You died")
            sys.exit()
        elif self.hp > self.max_hp:
            self.hp = self.max_hp

    def use_item(self, item_index: int):
        # if the item is food, remove it from inv, call its eat method with self as input
        if type(self.inventory[item_index]) == Food:
            food = self.inventory.pop(item_index)
            food.Eat(self)
