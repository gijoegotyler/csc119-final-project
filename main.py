# CSC119-680
# Tyler Wright
# 2/9/2022

# Library Imports
import math
import random
import sys
from typing import List, Union

# Import Classes
from enemy import Enemy
from items import Food, Sword
from player import Player
from room import Room

# define constants for board size and generate 2D array of board size
board_size = (5, 5)
board = [[Room() for j in range(board_size[1])] for i in range(board_size[0])]

# set start to (0,0) and added to the list of used indexes
start_index = (0, 0)
used_indexes = [start_index]

# make a tmp var and map of Directions to Tuples
tmp_index = (0, 0)
dir_map = {"East": (0, 1), "West": (0, -1), "North": (-1, 0), "South": (1, 0)}
dir_opposite = {"East": "West", "West": "East", "North": "South", "South": "North"}

# get the total number of rooms
number_of_rooms = board_size[0] * board_size[1]

# loop through random number of rooms from floor of one third of the rooms to all the rooms
for i in range(random.randrange(number_of_rooms // 3, number_of_rooms)):
    # generate temp list of directions
    dirs = []

    # add direction to possible directions if it won't move off the map
    if not (tmp_index[1] + 1 >= 5):
        dirs.append("East")
    if not (tmp_index[1] - 1 < 0):
        dirs.append("West")
    if not (tmp_index[0] + 1 >= 5):
        dirs.append("South")
    if not (tmp_index[0] - 1 < 0):
        dirs.append("North")

    # pick a random direction and calculate the index of the room the program is moving to
    opt = random.randrange(0, len(dirs))
    new_index = (
        tmp_index[0] + dir_map[dirs[opt]][0],
        tmp_index[1] + dir_map[dirs[opt]][1],
    )

    # skip this cycle if we are back tracking
    if new_index in used_indexes:
        continue

    # tell the rooms that they are now neighbors
    board[tmp_index[0]][tmp_index[1]].add_neighbor(dirs[opt], new_index)
    board[new_index[0]][new_index[1]].add_neighbor(dir_opposite[dirs[opt]], tmp_index)

    # make the new index the tmp index and add it to the used list
    tmp_index = new_index
    used_indexes.append(tmp_index)

# set end to True for final room
board[used_indexes[len(used_indexes) - 1][0]][
    used_indexes[len(used_indexes) - 1][1]
].end = True


def generateItems(steps: int) -> List[Union[Food, Sword]]:
    # generate better items for more steps
    items: List[Union[Food, Sword]] = []

    while random.randrange(1, (51 + (len(items) * 5)) - steps) < 20:
        if random.randrange(1, 6) > 3:
            # generate sword (balanced, durable, powerful)
            tn = random.randrange(1, 4)

            if tn == 1:
                # balanced - reason damage and durability
                name = random.choice(
                    ["Elucidator", "Mate Chopper", "Lambent Light", "Excalibur"]
                )
                dmg = random.randrange(steps * 3, steps * 5)
                dur = random.randrange(dmg * 5, dmg * 7)
            elif tn == 2:
                # durable - extreme durability low damage
                name = random.choice(
                    ["Stick", "Iron Pipe", "Night Sky Sword", "Liberator"]
                )
                dmg = random.randrange(steps, steps * 2)
                dur = random.randrange(dmg * 10, dmg * 20)
            else:
                # glass - high damage low durability
                name = random.choice(
                    [
                        "Glass Shard",
                        "Dark Repulser",
                        "Ice Rose Sword",
                        "Fragant Olive Sword",
                    ]
                )
                dmg = random.randrange(steps * 9, steps * 12)
                dur = random.randrange(dmg, dmg * 2)

            items.append(Sword(name, dmg, dur))
        else:
            # generate food
            name = random.choice(["Apple", "Orange", "Banana", "Cherry", "Grape"])
            healing_factor = random.randrange(steps, steps * 3)

            items.append(Food(name, healing_factor))

    return items


def generateEnemies(steps: int) -> List[Enemy]:
    # give stronger enemies for more steps
    enemies: List[Enemy] = []

    while random.randrange(1, (51 + steps * 2) - (len(enemies) * 3)) > 25:
        # generate enemies
        name = random.choice(["Goblin", "Orc", "Troll", "Giant", "Dragon"])
        en = random.randrange(1, 4)

        if en == 1:
            # health
            health = random.randrange(steps * 2, steps * 3)
            power = random.randrange(math.ceil(steps * 0.5), steps)
        elif en == 2:
            # power
            health = random.randrange(math.ceil(steps * 0.5), steps)
            power = random.randrange(steps * 2, steps * 3)
        else:
            # health and power
            health = random.randrange(steps, steps * 2)
            power = random.randrange(steps, steps * 2)

        enemies.append(Enemy(name, health, power))

    return enemies


# give adjacent rooms chance to connect if its not already connected
# loop through all rooms
for i in range(board_size[0]):
    for j in range(board_size[1]):
        # if room is used
        if (i, j) in used_indexes:
            if random.randrange(1, 2000) == 1337:
                board[i][j].ladder = True

            if used_indexes.index((i, j)) != 0:
                board[i][j].chest = generateItems(used_indexes.index((i, j)) + 2)
                board[i][j].enemies = generateEnemies(used_indexes.index((i, j)) + 2)

            # get existing neighbors
            dirs = list(board[i][j].neighbors)

            # for each dir
            for d in ["North", "East", "South", "West"]:
                # if there is already a neighbor in that dir, skip
                if d in dirs:
                    continue

                # calculate new pos of new neighbor
                pot_n = (i + dir_map[d][0], j + dir_map[d][1])

                # if the pos new neighbor is not a used pos, skip
                if pot_n not in used_indexes:
                    continue

                # if random num between 1 and 10 is greater than 7 (30% chance) connect rooms
                if random.randrange(1, 11) > 7:
                    board[i][j].add_neighbor(d, pot_n)
                    board[pot_n[0]][pot_n[1]].add_neighbor(dir_opposite[d], (i, j))


# make the player
player = Player()

player.inventory.append(Sword("Stick", 5, 30))
player.inventory.append(Food("Apple", 5))

# set current room var
current_room = start_index

# make visited indexes list so it can start to give users hints if they go in circles
visited_rooms = []

# game intro text
print("Welcome to Mahō no Shōnen no Bōken")
print()


def move():
    global current_room
    global visited_rooms
    global board
    global player

    # get list of dirs that have neighbors in current room
    dirs = list(board[current_room[0]][current_room[1]].neighbors)

    # print direction options
    print()
    print("You enter the room and see doors in the following directions:")
    for d in dirs:
        print(f"{d}")

    # get user input on which dir and format to title case
    move_dir = input("Which way do you move: ").title()

    if (move_dir == "Climb" or move_dir == "Up") and board[current_room[0]][
        current_room[1]
    ].ladder == True:
        print(
            "You calmly scale the old ladder, at the top you notice that the ceiling tile can be pushed up."
        )
        print("You push up the ceiling tile and climb on top of the roof.")
        print("Congrats you have found the secret exit.")
        sys.exit()

    # change the current room
    visited_rooms.append(current_room)
    current_room = board[current_room[0]][current_room[1]].neighbors[move_dir]

    # give hint if user visited room three or more times
    if visited_rooms.count(current_room) > 2:
        print()
        print("This room is strangely familiar")

    if board[current_room[0]][current_room[1]].ladder == True:
        print("There's a rickety ladder in the corner of the room.")

    # tell user which way they moved
    print()
    print(f"You moved {move_dir}")
    print()
    print(f"You have {player.hp}HP left")
    print()


def fight():
    global player
    global board

    enemies = board[current_room[0]][current_room[1]].enemies

    for enemy in enemies:
        print(f"You see a {enemy.name} ({enemy.health}HP/{enemy.power}ATK)")
        print()
        print(f"You have {player.hp}HP")
        print()
        while enemy.health > 0:
            choice = input("1) Use an item\n2) Attack\nWhat do you do? ").title()
            print()

            if "1" in choice:
                player.use_item()
            else:
                enemy.health -= player.attack()
                if enemy.health <= 0:
                    player.experience += max(enemy.power, enemy.health)
                    player.check_level_up()
                    continue

            print("The enemy attacks")
            player.damage(enemy.power)
            player.check_hp()
            print(f"You have {player.hp}HP left")

    board[current_room[0]][current_room[1]].enemies = []


def menu():
    global player

    print("1) Move\n2) View Inventory\n3) View Skills")
    selection = int(input("What would you like to do? "))
    if selection == 1:
        move()
    elif selection == 2:
        player.show_inventory()
    else:
        player.show_skills()


# main game loop
while True:

    menu()

    # if player is in a room with enemies
    if board[current_room[0]][current_room[1]].enemies:
        fight()

    if board[current_room[0]][current_room[1]].chest:
        print("You find a chest")
        print("You open the chest and find:")
        for item in board[current_room[0]][current_room[1]].chest:
            print(f"{item.name}")
            player.inventory.append(item)
        board[current_room[0]][current_room[1]].chest = []

    # check if they made it to the end
    if board[current_room[0]][current_room[1]].end:
        print()
        print("Congrats you made it to the end")
        sys.exit()

    print()
