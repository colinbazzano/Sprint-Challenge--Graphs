from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


from util import Queue
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

opposite_directions = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}


def dft_recursive(starting_room):

    def dft_helper(room, visited):
        visited.add(room.id)  # add the first room
        path = []  # keep track of our path

        for direction in room.get_exits():  # appends available directions if direction_to is not None
            # returns direction_to if there is one
            next_room = room.get_room_in_direction(direction)
            if next_room.id not in visited:  # if we have no visited the room in question
                # call the helper on that room
                next_room_path = dft_helper(next_room, visited)
                if next_room_path:
                    print("Path of next room:", next_room_path)
                    new_path = [direction, *next_room_path,
                                opposite_directions[direction]]
                else:
                    new_path = [direction, opposite_directions[direction]]
                path = [*path, *new_path]
        return path

    visited = set()
    path = dft_helper(starting_room, visited)
    print("Path:", path)

    return path


traversal_path = dft_recursive(player.current_room)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
