import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from collections import deque
from Lab_2.Task_1.Code_Sample.search_algorithm import PriorityQueue

'''Generates a random 2d map with a rotated-H-shape object in the middle and obstacles (small blocks) randomly distributed. 
    You can specify any size of this map but your solution has to be independent of map size

Parameters:
-----------
size_ : list
    Width and height of the 2d grid map, e.g. [60, 60]. The height and width of the map shall be greater than 40.

Returns:
--------
    map2d : array-like, shape (size_[0], size_[1])
        A 2d grid map, cells with a value of 0: Free cell; 
                                            -1: Obstacle;
                                            -2: Start point;
                                            -3: Goal point;
                                        
    [ytop, ybot, minx] : list
        information of the rotated-H-shape object
        ytop - y coordinate of the top horizontal wall/part
        ybot - y coordinate of the bottom horizontal wall/part
        minx - X coordinate of the vertical wall 
'''
# helper
def manhattan_distance(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def euclidean_distance(current, goal):
    return np.sqrt((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2)

def make_custom_heuristic(map2d, obstacle_info):

    ytop, ybot, minx = obstacle_info

    rows, cols = map2d.shape

    # Infer maxx from the map without modifying the generator.
    # The vertical wall occupies these columns throughout
    # the interior rows between the horizontal walls.
    wall_rows = map2d[ybot + 1:ytop, :]
    fully_blocked = np.all(wall_rows == -1, axis=0)

    maxx = minx

    while maxx < cols and fully_blocked[maxx]:
        maxx += 1

    # Build a simplified map containing only the vertical wall.
    # Ignore all random obstacles and horizontal wall extensions.
    # This creates a less restrictive version of the real map.
    relaxed_map = np.zeros((rows, cols), dtype=int)
    relaxed_map[ybot:ytop, minx:maxx] = -1

    # Precompute shortest distances from the goal using BFS.
    distances = np.full((rows, cols), np.inf)

    goal = tuple(np.argwhere(map2d == -3)[0])

    distances[goal] = 0

    frontier = deque([goal])

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    while frontier:

        current = frontier.popleft()
        row, col = current

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if (0 <= nr < rows and
                0 <= nc < cols and
                relaxed_map[nr, nc] != -1 and
                np.isinf(distances[nr, nc])):

                distances[nr, nc] = distances[row, col] + 1
                frontier.append((nr, nc))

    # Return a heuristic compatible with A_star_search().
    def heuristic(current, goal):
        return distances[current]

    return heuristic

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

def A_star_search(map, start, goal, obstacle_info, heuristic, make_custom_heuristic=None):

    if make_custom_heuristic is not None:
        heuristic = make_custom_heuristic(map, obstacle_info)

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

    expanded_nodes = 0

    closed_set = set()  # To track unique expanded nodes


    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()

        if current in closed_set:
            continue  # Skip if the node has already been expanded
        # This is because the heuristic is consistent, so the first time we expand a node, we have found the optimal path to it.
        # f(n) = g(n) + h(n), where g(n) is the cost to reach n and h(n) is the heuristic estimate from n to the goal.
        # h(n) <= h(n') + c(n, n'), where n' is a neighbor of n and c(n, n') is the cost to move from n to n'.
        # => If we expand a node n, we have found the optimal path to it, and any subsequent paths to n will be longer or equal in cost.

        expanded_nodes += 1
        closed_set.add(current)

        # check if the goal is reached
        if current == goal:
            break

        # for each neighbour of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!)
        for neighbor in get_neighbors(map, current):

            new_cost = cost[current] + moving_cost  # Compute the cost to reach the neighbor

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                # Implement cost function
                neighbor_cost = heuristic(neighbor, goal)
                priority = new_cost + neighbor_cost  # Total cost = cost to reach neighbor + heuristic
                frontier.add(neighbor, priority)
                # add to path
                came_from[neighbor] = current



    if goal not in came_from:
        return None, float('inf'), expanded_nodes  # Return None and infinite cost if the goal is not reachable
    
    path = reconstruct_path(came_from, start, goal)
    
    return path, cost[goal], expanded_nodes