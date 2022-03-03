# CSC119-680
# Tyler Wright
# 2/9/2022

# import libraries
import math
import random
import sys
from typing import Optional


# define player class
class Player:
    # initialize player class
    def __init__(self):
        # set base skill values
        self.skills = {
            "Strength": 2,
            "Speed": 2,
            "Defense": 2,
            "Intelligence": 3,
            "Vitality": 3,
            "Magic": None,
            "Crafting": None,
        }

        # set base hp and max hp
        self.max_hp = self.skills["Vitality"] * 5
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
        if list(self.skills)[selection] == "Vitality":
            prev_max_hp = self.max_hp
            self.max_hp = self.skills["Vitality"] * 5
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

    def show_inventory(self):
        print()
        for i in self.inventory:
            if i.action == "Eat":
                print(f"{i.name} Heals {i.healing}HP")
            else:
                print(
                    f"{i.name} Deals {i.power} damage and has {i.durability} durability"
                )

    def show_skills(self):
        print()
        for i in self.skills:
            if self.skills[i] is not None:
                print(f"{i} Level: {self.skills[i]}")

    def list_items(self):
        items = [i for i in self.inventory if i.action != "Attack"]
        for i in range(len(items)):
            print(f"{i+1}) {items[i].name} - {items[i].action}")
        return items

    def use_item(self):
        items = self.list_items()
        choice = int(input("Which item do you use: ")) - 1
        item_index = self.inventory.index(items[choice])

        if self.inventory[item_index].action == "Eat":  # type: ignore
            food = self.inventory.pop(item_index)
            self.hp += food.healing
            print(f"You eat a {food.name} and heal for {food.healing}HP")
            self.check_hp()
            print(f"You have {self.hp}HP")

    def attack(self):
        use_magic = "No"
        if self.skills["Magic"] is not None and self.skills["Magic"] >= 1:
            use_magic = input("Would you like to use magic (Yes/No): ")

        if "y" in list(use_magic.lower()):
            # write the magic code
            print("magic")
        else:
            weapons_indices = [
                i
                for i in range(len(self.inventory))
                if self.inventory[i].action == "Attack"
            ]

            for i in range(len(weapons_indices)):
                print(
                    f"{i+1}) {self.inventory[weapons_indices[i]].name} ({self.inventory[weapons_indices[i]].power}DMG/{self.inventory[weapons_indices[i]].durability}DUR)"
                )
            weapon_choice = input("What weapon will you use: ")
            weapon_index = weapons_indices[int(weapon_choice) - 1]

            self.inventory[weapon_index].damage_item()

            strength = self.skills["Strength"]

            print(
                f"You attacked with {self.inventory[weapon_index].name}, and dealt {self.inventory[weapon_index].power * strength} damage"
            )

            if self.inventory[weapon_index].check_durabiliy() == "Broken":
                print(f"{self.inventory[weapon_index]} broke.")
                self.inventory.pop(weapon_index)

            return self.inventory[weapon_index].power * strength

    def damage(self, power: int):
        if random.randrange(1, 75) < 2 * self.skills["Speed"]:
            print("You managed to dodge the attack")
        else:
            dmg = power - self.skills["Defense"]
            self.hp -= dmg
            print(f"You take {dmg} damage")
