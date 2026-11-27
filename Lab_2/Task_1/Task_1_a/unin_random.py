# An example of search algorithm, feel free to modify and implement the missing part
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

import random

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
def get_neighbors(map, current):
    current_x, current_y = current
    rows, cols = map.shape
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        neighbor_x, neighbor_y = current_x + dx, current_y + dy
        if 0 <= neighbor_x < rows and 0 <= neighbor_y < cols and map[neighbor_x][neighbor_y] != -1:  # Check if the neighbor is not an obstacle
            neighbors.append((neighbor_x, neighbor_y))
    return neighbors

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
def randomS(map, start, goal):

    # cost moving to another cell
    moving_cost = 1
    # open list
    frontier = [start]
    # explored nodes
    explored = set()
    # current path
    came_from = {start: None}
    # current cost
    cost = {start: 0}

    expanded_nodes = 0

    while frontier:
        current = random.choice(frontier)
        frontier.remove(current)
        explored.add(current)
        expanded_nodes += 1
        if current == goal:
            break
        
        for neighbor in get_neighbors(map, current):
            if neighbor is None:
                continue

            neighbor_x, neighbor_y = neighbor
            neighbor_value = map[neighbor_x][neighbor_y]
            # Check if the neighbor is not in explored, not in frontier, and is not an obstacle
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
                came_from[neighbor] = current
                cost[neighbor] = cost[current] + moving_cost

    if goal not in came_from:
        return None, float('inf'), expanded_nodes  # Return None and infinite cost if the goal is not reachable
    
    path = reconstruct_path(came_from, start, goal)
    
    return path, cost[goal], expanded_nodes