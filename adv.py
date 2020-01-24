from room import Room
from player import Player
from world import World
from util import Stack, Queue
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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



visited_rooms = set()
player.current_room = world.starting_room
# visited_rooms.add(player.current_room)





######
# UNCOMMENT TO WALK AROUND
######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


graph = {}

def find_fastest_path(current_room, next_room):
    visited = {}

    # Create an empty queue and enqueue the starting vertex ID
    q = Queue()
    q.enqueue([current_room])

    # While the queue is not empty...
    while next_room not in visited:
        # Dequeue the first path
        path = q.dequeue()
        # Look at the last user in the path...
        current_room = path[-1]
        # If the user has not been visited
        if current_room not in visited:
            # Mark as visited and add their path
            visited[current_room] = path
            # Add a path to each neighbor to the queue
            for direction in graph[current_room]:
                if graph[current_room][direction] != '?':
                    new_path = path.copy()
                    new_path.append(graph[current_room][direction])
                    q.enqueue(new_path)


    return visited[next_room]
    

def reverse_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 'e':
        return 'w'
    elif direction == 's':
        return 'n'
    elif direction == 'w':
        return 'e'
    else:
        print('bad direction ', direction)


unvisited = Stack()
last_room = [0,'direction']


while len(visited_rooms) != len(room_graph):
    
    
    if player.current_room.id not in graph:
        graph[player.current_room.id] = {}
        for direction in player.current_room.get_exits():
            if direction == last_room[1]:
                # change unknown direction in last room to this room
                graph[last_room[0]][reverse_direction(last_room[1])] = player.current_room.id
                #change unknown direction in this room to last room
                graph[player.current_room.id][direction] = last_room[0]

            else:
                graph[player.current_room.id][direction] = '?'
    else:
        # change unknown direction in last room to this room
        graph[last_room[0]][reverse_direction(last_room[1])] = player.current_room.id
        #change unknown direction in this room to last room
        graph[player.current_room.id][last_room[1]] = last_room[0]


    #add all unexplored neighbors to unvisited
    if player.current_room not in visited_rooms:

        if 'e' in graph[player.current_room.id] and graph[player.current_room.id]['e'] == '?':    
            unvisited.push((player.current_room.id, 'e'))

        if 'n' in graph[player.current_room.id] and graph[player.current_room.id]['n'] == '?':    
            unvisited.push((player.current_room.id, 'n'))

        if 'w' in graph[player.current_room.id] and graph[player.current_room.id]['w'] == '?':    
            unvisited.push((player.current_room.id, 'w'))

        if 's' in graph[player.current_room.id] and graph[player.current_room.id]['s'] == '?':    
            unvisited.push((player.current_room.id, 's'))



    visited_rooms.add(player.current_room)
    next_room = unvisited.pop()
    # print('next room ',next_room)

    if not next_room:
        print('problem with next room:', next_room)
        break

    # change last room
    last_room[0] = player.current_room.id
    last_room[1] = reverse_direction(next_room[1])

    # move player into next room
    if player.current_room.id == next_room[0]:
        
        # print('traveled vs total', len(visited_rooms), len(room_graph))
        player.travel(next_room[1])
        traversal_path.append(next_room[1])
    else:
        # print('***not in the right room***')
        # find the fastest path back to that room and then travel there.
        #and then: player.travel(next_room[1])
        fastest_path = find_fastest_path(player.current_room.id, next_room[0])[1:]
        
        for room in fastest_path:

            # print('fastest',fastest_path, graph[player.current_room.id])
            if 'n' in graph[player.current_room.id] and graph[player.current_room.id]['n'] == room:
                last_room[0] = player.current_room.id
                last_room[1] = reverse_direction('n')
                player.travel('n')
                traversal_path.append('n')

            elif 'e' in graph[player.current_room.id] and graph[player.current_room.id]['e'] == room:
                last_room[0] = player.current_room.id
                last_room[1] = reverse_direction('e')
                player.travel('e')
                traversal_path.append('e')

            elif 's' in graph[player.current_room.id] and graph[player.current_room.id]['s'] == room:
                last_room[0] = player.current_room.id
                last_room[1] = reverse_direction('s')
                player.travel('s')
                traversal_path.append('s')

            elif 'w' in graph[player.current_room.id] and graph[player.current_room.id]['w'] == room:
                last_room[0] = player.current_room.id
                last_room[1] = reverse_direction('w')
                player.travel('w')
                traversal_path.append('w')

            else:
                print('error line 162', room)
                break
            
        unvisited.push(next_room)








# TRAVERSAL TEST


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# for i in range(len(room_graph)):
#     print(i, graph[i])