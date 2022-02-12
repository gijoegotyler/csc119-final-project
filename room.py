# CSC119-680
# Tyler Wright
# 2/9/2022

# import libraries
from typing import Tuple

# define Room Class
class Room:
    # set basic room property of  neighbors
    def __init__(self):
        self.neighbors = {}
        self.end = False

    # create function to add a neighbor
    def add_neighbor(self, direction: str, room_index: Tuple[int, int]):
        self.neighbors.update({direction: room_index})
