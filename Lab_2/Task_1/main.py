import random

import numpy as np
import matplotlib.pyplot as plt
from Code_Sample import path_planning as pp
import unin_random as unin_ran
import unin_BFS as BFS
import unin_DFS as DFS
import in_greedy as greedy
import in_astar as astar
import validation as val


def init_map(size_):
    new_map = pp.generateMap2d(size_)
    print(f"Map size: {size_[0]} x {size_[1]}")
    start_point = (np.where(new_map == -2)[0][0], np.where(new_map == -2)[1][0])
    goal_point = (np.where(new_map == -3)[0][0], np.where(new_map == -3)[1][0])
    start_point = tuple(map(int, start_point))
    goal_point = tuple(map(int, goal_point))
    print(f"Start point: {start_point}")
    print(f"Goal point: {goal_point}")
    return new_map, start_point, goal_point

def formatting(search_pf=False):
    path, cost, expanded_nodes = search_pf()
    print("\n===== SEARCH RESULTS =====")
    print(f"Path length: {len(path) - 1}")
    print(f"Total cost: {cost}")
    print(f"expanded nodes: {expanded_nodes}")
    print(f"Number of positions: {len(path)}")
    print("\nPath:")
    path = np.array(path)
    for i, position in enumerate(path):
        print(f"Step {i}: {position}")
    return (path, cost, expanded_nodes)

def plot_path(map, path, title_="Path Planning"):
    # Convert only for visualization
    plot_path = np.asarray(path)[:, ::-1]
    pp.plotMap(map, plot_path, title_=title_)

if __name__ == "__main__":
    size_x, size_y = random.randint(20, 100), random.randint(20, 100)
    new_map, start_point, goal_point = init_map([size_x, size_y])

    search_func = input("Enter the search function to use (random, BFS, DFS, greedy, astar): ").strip().lower()
    heuristic_choice = None

    match search_func:
        case "greedy":
            heuristic_choice = input("Enter the heuristic to use (eucl, manh): ").strip().lower()
            if heuristic_choice not in ["eucl", "manh"]:
                print("Invalid heuristic choice. Please choose 'euclidean' or 'manhattan'.")
                exit(1)
            elif heuristic_choice == "eucl":
                greedy_path_euclidean, greedy_cost_euclidean, greedy_expanded_nodes = formatting(search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, heuristic=greedy.euclidean_distance))
                val.validate_path(new_map, greedy_path_euclidean, start_point, goal_point)
                plot_path(new_map, greedy_path_euclidean, title_="Greedy Search with Euclidean Heuristic")
            elif heuristic_choice == "manh":
                greedy_path_manhattan, greedy_cost_manhattan, greedy_expanded_nodes = formatting(search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, heuristic=greedy.manhattan_distance))
                val.validate_path(new_map, greedy_path_manhattan, start_point, goal_point)
                plot_path(new_map, greedy_path_manhattan, title_="Greedy Search with Manhattan Heuristic")
        case "astar":
            heuristic_choice = input("Enter the heuristic to use (eucl, manh): ").strip().lower()
            if heuristic_choice not in ["eucl", "manh"]:
                print("Invalid heuristic choice. Please choose 'euclidean' or 'manhattan'.")
                exit(1)
            elif heuristic_choice == "eucl":
                astar_path_euclidean, astar_cost_euclidean, astar_expanded_nodes = formatting(search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, heuristic=astar.euclidean_distance))
                val.validate_path(new_map, astar_path_euclidean, start_point, goal_point)
                plot_path(new_map, astar_path_euclidean, title_="A* Search with Euclidean Heuristic")
            elif heuristic_choice == "manh":
                astar_path_manhattan, astar_cost_manhattan, astar_expanded_nodes = formatting(search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, heuristic=astar.manhattan_distance))
                val.validate_path(new_map, astar_path_manhattan, start_point, goal_point)
                plot_path(new_map, astar_path_manhattan, title_="A* Search with Manhattan Heuristic")
        case "random":
            print("Random search selected. Note: This may not find a path in some cases.")
            rand_path, rand_cost, rand_expanded_nodes = formatting(search_pf=lambda: unin_ran.randomS(map=new_map, start=start_point, goal=goal_point))
            val.validate_path(new_map, rand_path, start_point, goal_point)
            plot_path(new_map, rand_path, title_="Random Search")
        case "bfs":
            print("BFS search selected.")
            BFS_path, BFS_cost, BFS_expanded_nodes = formatting(search_pf=lambda: BFS.BFS(map=new_map, start=start_point, goal=goal_point))
            val.validate_path(new_map, BFS_path, start_point, goal_point)
            plot_path(new_map, BFS_path, title_="Breadth-First Search")
        case "dfs":
            print("DFS search selected.")
            DFS_path, DFS_cost, DFS_expanded_nodes = formatting(search_pf=lambda: DFS.DFS(map=new_map, start=start_point, goal=goal_point))
            val.validate_path(new_map, DFS_path, start_point, goal_point)
            plot_path(new_map, DFS_path, title_="Depth-First Search")


