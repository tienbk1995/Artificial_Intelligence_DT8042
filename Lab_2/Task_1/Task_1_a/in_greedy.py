import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from sys import path
import numpy as np
from Lab_2.Task_1.Code_Sample.search_algorithm import PriorityQueue
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
def manhattan_distance(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def euclidean_distance(current, goal):
    return np.sqrt((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2)

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

def greedy_search(map, start, goal, heuristic):

    start_cost = heuristic(start, goal)  # Calculate heuristic for the start node

    # cost moving to another cell
    moving_cost = 1

    # open list
    frontier = PriorityQueue()
    # add starting cell to open list
    frontier.add(start, start_cost)

    # path taken
    came_from = {start: None}

    # expanded list with cost value for each cell
    cost = {start: 0}

    # list of visited nodes
    visited = [start]

    expanded_nodes = 0


    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()

        expanded_nodes += 1

        # check if the goal is reached
        if current == goal:
            break

        # for each neighbour of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!)
        for neighbor in get_neighbors(map, current):

            if neighbor in visited:
                continue

            visited.append(neighbor)
            # compute cost to reach next cell
            # Implement cost function
            neighbor_cost = heuristic(neighbor, goal)

            # add next cell to open list
            frontier.add(neighbor, neighbor_cost)
            
            # add to path
            came_from[neighbor] = current

            # update the cost of moving from start to the neighbor
            cost[neighbor] = cost[current] + moving_cost


    if goal not in came_from:
        return None, float('inf'), expanded_nodes  # Return None and infinite cost if the goal is not reachable
    
    path = reconstruct_path(came_from, start, goal)
    
    return path, cost[goal], expanded_nodes