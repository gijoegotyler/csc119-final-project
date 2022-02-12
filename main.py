# CSC119-680
# Tyler Wright
# 2/9/2022

# Library Imports
import sys
import math
import random

# Import Classes
from items import Food
from items import Sword
from player import Player
from room import Room

# define constants for board size and generate 2D array of board size
board_size = (5,5)
board = [[Room() for j in range(board_size[1])] for i in range(board_size[0])]

# set start to (0,0) and added to the list of used indexes
start_index = (0,0)
used_indexes = [start_index]

# make a tmp var and map of Directions to Tuples
tmp_index = (0,0)
dir_map = {"East": (0, 1), "West": (0, -1), "North": (-1, 0), "South":(1, 0)}
dir_opposite = {"East": "West", "West": "East", "North": "South", "South": "North"}

# get the total number of rooms
number_of_rooms = board_size[0] * board_size[1]

# loop through random number of rooms from floor of one third of the rooms to all the rooms
for i in range(random.randrange(number_of_rooms//3,number_of_rooms)):
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
    opt = random.randrange(0,len(dirs))
    new_index = (tmp_index[0] + dir_map[dirs[opt]][0], tmp_index[1] + dir_map[dirs[opt]][1])

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
board[used_indexes[len(used_indexes)-1][0]][used_indexes[len(used_indexes)-1][1]].end = True

# give adjacent rooms chance to connect if its not already connected
# loop through all rooms 
for i in range(board_size[0]):
    for j in range(board_size[1]):
        # if room is used
        if (i,j) in used_indexes:
            # get existing neighbors
            dirs = list(board[i][j].neighbors)

            # for each dir
            for d in ["North", "East", "South", "West"]:
                # if there is already a neighbor in that dir, skip
                if d in dirs:
                    continue
                
                # calculate new pos of new neighbor
                pot_n = (i+dir_map[d][0],j+dir_map[d][1])
                
                # if the pos new neighbor is not a used pos, skip 
                if pot_n not in used_indexes:
                    continue

                # if random num between 1 and 10 is greater than 7 (30% chance) connect rooms
                if random.randrange(1,11) > 7:
                    board[i][j].add_neighbor(d, pot_n)
                    board[pot_n[0]][pot_n[1]].add_neighbor(dir_opposite[d], (i,j))


# make the player 
player = Player()

# set current room var
current_room = start_index

# make visited indexes list so it can start to give users hints if they go in circles
visited_rooms = [] 

# game intro text
print("Welcome to Mahō no Shōnen no Bōken")
print()

# main game loop
while True:
    # get list of dirs that have neighbors in current room
    dirs = list(board[current_room[0]][current_room[1]].neighbors)
    
    # print direction options
    print("You enter the room and see doors in the following directions:")
    for i in dirs:
        print(f"{i}")

    # get user input on which dir and format to title case
    move_dir = input("Which way do you move: ").title()

    # change the current room
    visited_rooms.append(current_room)
    current_room = board[current_room[0]][current_room[1]].neighbors[move_dir]

    # give hint if user visited room three or more times
    if visited_rooms.count(current_room) > 2:
        print()
        print("This room is strangely familiar")
    
    # tell user which way they moved
    print()
    print(f"You moved {move_dir}")

    # check if they made it to the end
    if board[current_room[0]][current_room[1]].end:
        print()
        print("Congrats you made it to the end")
        sys.exit()

    print()
