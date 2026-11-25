# An example of search algorithm, feel free to modify and implement the missing part
import random
import numpy as np

'''Generates a random 2d map with obstacles (small blocks) randomly distributed. 
    You can specify any size of this map but your solution has to be independent of map size

Parameters:
-----------
size_ : list
    Width and height of the 2d grid map, e.g. [60, 60]. The height and width of the map shall be greater than 20.

Returns:
--------
    map2d : array-like, shape (size_[0], size_[1])
        A 2d grid map, cells with a value of 0: Free cell; 
                                            -1: Obstacle;
                                            -2: Start point;
                                            -3: Goal point;
'''
# helper
def get_neighbors(current):
    current_x, current_y = current
    if current_y == 0 and current_x == 0:
        up_curr_node = None
        down_curr_node = (current_x+1, current_y)
        left_curr_node = None
        right_curr_node = (current_x, current_y+1)
    elif current_y == 0 and current_x == 59:
        up_curr_node = (current_x-1, current_y)
        down_curr_node = None
        left_curr_node = None
        right_curr_node = (current_x, current_y+1)
    elif current_y == 59 and current_x == 0:
        up_curr_node = None
        down_curr_node = (current_x+1, current_y)
        left_curr_node = (current_x, current_y-1)
        right_curr_node = None
    elif current_y == 59 and current_x == 59:
        up_curr_node = (current_x-1, current_y)
        down_curr_node = None
        left_curr_node = (current_x, current_y-1)
        right_curr_node = None
    elif current_y == 0:
        up_curr_node = (current_x-1, current_y)
        down_curr_node = (current_x+1, current_y)
        left_curr_node = None
        right_curr_node = (current_x, current_y+1)
    elif current_y == 59:
        up_curr_node = (current_x-1, current_y)
        down_curr_node = (current_x+1, current_y)
        left_curr_node = (current_x, current_y-1)
        right_curr_node = None
    elif current_x == 0:
        up_curr_node = None
        down_curr_node = (current_x+1, current_y)
        left_curr_node = (current_x, current_y-1)
        right_curr_node = (current_x, current_y+1)
    elif current_x == 59:
        up_curr_node = (current_x-1, current_y)
        down_curr_node = None
        left_curr_node = (current_x, current_y-1)
        right_curr_node = (current_x, current_y+1)
    else:
        up_curr_node = (current_x-1, current_y)
        down_curr_node = (current_x+1, current_y)
        left_curr_node = (current_x, current_y-1)
        right_curr_node = (current_x, current_y+1)
    return [up_curr_node, down_curr_node, left_curr_node, right_curr_node]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path

# random search algorithm
def random_search(map):

    start = (np.where(map == -2)[0][0], np.where(map == -2)[1][0])
    goal = (np.where(map == -3)[0][0], np.where(map == -3)[1][0])   

    # cost moving to another cell
    moving_cost = 1
    # open list
    frontier = [start]
    # explored nodes
    explored = set()
    # current path
    came_from = {}
    # current cost
    cost = {start: 0}

    while frontier:
        current = random.choice(frontier)
        frontier.remove(current)
        explored.add(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return path, cost[current]
        
        for neighbor in get_neighbors(current):
            if neighbor is None:
                continue

            neighbor_x, neighbor_y = neighbor
            neighbor_value = map[neighbor_x][neighbor_y]

            if neighbor not in explored and neighbor not in frontier and neighbor_value != -1:
                frontier.append(neighbor)
                came_from[neighbor] = current
                cost[neighbor] = cost[current] + moving_cost
    return None