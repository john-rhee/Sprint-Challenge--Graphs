from room import Room
from player import Player
from world import World
from util import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
traversal_path = []
visited = {}

def move_to(direction):
    player.travel(direction)
    traversal_path.append(direction)

def backward_exits(to):
    if to == "n":
        return "s"
    elif to == "s":
        return "n"
    elif to == "e":
        return "w"
    elif to == "w":
        return "e"   

def adding_visited(current_room, exits):
    visited[current_room] = {}
    for i in exits:
        visited[current_room][i] = None           
    
def dft(current_room):
    current_room = player.current_room.id
    current_exits = player.current_room.get_exits()
    previous_room = None
    s = Stack()

    s.push([None, current_room, previous_room, current_exits])

    while len(visited) < 499:
        node = s.pop()
        direction = node[0]
        current_room = node[1]
        previous_room = node[2]
        current_exits = node[3]

        if current_room not in visited:
            adding_visited(current_room, current_exits)

        if direction != None:
            visited[current_room][backward_exits(direction)] = previous_room

        if previous_room != None:
            visited[previous_room][direction] = current_room

        for i in visited[current_room].keys():
            if visited[current_room][i] == None:
                s.push(node)
                previous = player.current_room.id                
                move_to(i)
                s.push([i, player.current_room.id, previous, player.current_room.get_exits()])
                break

        if current_room == player.current_room.id:
            move_to(backward_exits(direction))
                      
dft(player.current_room.id)                

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
