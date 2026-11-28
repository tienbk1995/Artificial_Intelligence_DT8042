import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from Lab_2.Task_1.Code_Sample import path_planning as pp
import random
import numpy as np
import matplotlib.pyplot as plt
import unin_random as unin_ran
import unin_BFS as BFS
import unin_DFS as DFS
import in_greedy as greedy
import in_astar as astar
import validation as val
import main as main_module

if __name__ == "__main__":
    size_x, size_y = random.randint(20, 100), random.randint(20, 100)
    new_map, start_point, goal_point = main_module.init_map([size_x, size_y])

    greedy_path_euclidean, greedy_cost_euclidean, greedy_expanded_nodes_euclidean = main_module.formatting(search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, heuristic=greedy.euclidean_distance))
    val.validate_path(new_map, greedy_path_euclidean, start_point, goal_point)
    main_module.plot_path(new_map, greedy_path_euclidean, title_="Greedy Search with Euclidean Heuristic")

    greedy_path_manhattan, greedy_cost_manhattan, greedy_expanded_nodes_manhattan = main_module.formatting(search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, heuristic=greedy.manhattan_distance))
    val.validate_path(new_map, greedy_path_manhattan, start_point, goal_point)
    main_module.plot_path(new_map, greedy_path_manhattan, title_="Greedy Search with Manhattan Heuristic")

    astar_path_euclidean, astar_cost_euclidean, astar_expanded_nodes_euclidean = main_module.formatting(search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, heuristic=astar.euclidean_distance))
    val.validate_path(new_map, astar_path_euclidean, start_point, goal_point)
    main_module.plot_path(new_map, astar_path_euclidean, title_="A* Search with Euclidean Heuristic")

    astar_path_manhattan, astar_cost_manhattan, astar_expanded_nodes_manhattan = main_module.formatting(search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, heuristic=astar.manhattan_distance))
    val.validate_path(new_map, astar_path_manhattan, start_point, goal_point)
    main_module.plot_path(new_map, astar_path_manhattan, title_="A* Search with Manhattan Heuristic")

    rand_path, rand_cost, rand_expanded_nodes = main_module.formatting(search_pf=lambda: unin_ran.randomS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, rand_path, start_point, goal_point)
    main_module.plot_path(new_map, rand_path, title_="Random Search")

    BFS_path, BFS_cost, BFS_expanded_nodes = main_module.formatting(search_pf=lambda: BFS.BFS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, BFS_path, start_point, goal_point)
    main_module.plot_path(new_map, BFS_path, title_="Breadth-First Search")

    DFS_path, DFS_cost, DFS_expanded_nodes = main_module.formatting(search_pf=lambda: DFS.DFS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, DFS_path, start_point, goal_point)
    main_module.plot_path(new_map, DFS_path, title_="Depth-First Search")

    all_path_length = [len(greedy_path_euclidean) - 1, len(greedy_path_manhattan) - 1, len(astar_path_euclidean) - 1, len(astar_path_manhattan) - 1, len(rand_path) - 1, len(BFS_path) - 1, len(DFS_path) - 1]
    all_cost = [greedy_cost_euclidean, greedy_cost_manhattan, astar_cost_euclidean, astar_cost_manhattan, rand_cost, BFS_cost, DFS_cost]
    all_expanded_nodes = [greedy_expanded_nodes_euclidean, greedy_expanded_nodes_manhattan, astar_expanded_nodes_euclidean, astar_expanded_nodes_manhattan, rand_expanded_nodes, BFS_expanded_nodes, DFS_expanded_nodes]
    main_module.performance(all_path_length, all_cost, all_expanded_nodes)


