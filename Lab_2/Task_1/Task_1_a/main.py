import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from Lab_2.Task_1.Code_Sample import path_planning as pp
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

def plot_path(map, path=np.array([[xx, xx*2] if xx % 2 == 0 else [xx, xx+1] for xx in range(20)]), title_="Path Planning"):
    # Convert only for visualization
    plot_path = np.asarray(path)[:, ::-1]
    pp.plotMap(map, plot_path, title_=title_)

def performance(path_length=[ ], cost=[ ], expanded_nodes=[ ]):
    algo_names = [
        "Greedy (Euclidean)",
        "Greedy (Manhattan)",
        "A* (Euclidean)",
        "A* (Manhattan)",
        "Random",
        "BFS",
        "DFS",
    ]

    fig, axes = plt.subplots(1, 3, figsize=(14, 7))

    # Path Length
    axes[0].plot(range(len(algo_names)), path_length, marker='o')
    axes[0].set_title("Path Length")
    axes[0].set_xlabel("Search Algorithm")
    axes[0].set_ylabel("Length")
    axes[0].set_xticks(range(len(algo_names)))
    axes[0].set_xticklabels(algo_names, rotation=35, ha="right")

    # Total Cost
    axes[1].plot(range(len(algo_names)), cost, marker='o', color='orange')
    axes[1].set_title("Total Cost")
    axes[1].set_xlabel("Search Algorithm")
    axes[1].set_ylabel("Cost")
    axes[1].set_xticks(range(len(algo_names)))
    axes[1].set_xticklabels(algo_names, rotation=35, ha="right")

    # Expanded Nodes
    axes[2].plot(range(len(algo_names)), expanded_nodes, marker='o', color='green')
    axes[2].set_title("Expanded Nodes")
    axes[2].set_xlabel("Search Algorithm")
    axes[2].set_ylabel("Nodes")
    axes[2].set_xticks(range(len(algo_names)))
    axes[2].set_xticklabels(algo_names, rotation=35, ha="right")

    plt.tight_layout()
    plt.show()

def calculate_performance_metrics(path_length_list=[ ], cost_list=[ ], expanded_nodes_list=[ ]):
    algo_names = [
        "Greedy (Euclidean)",
        "Greedy (Manhattan)",
        "A* (Euclidean)",
        "A* (Manhattan)",
        "Random",
        "BFS",
        "DFS",
    ]
    path_length_avg = []
    cost_avg = []
    expanded_nodes_avg = []

    for algo_idx in range(len(algo_names)):
        path_length_avg_algo = sum(test[algo_idx] for test in path_length_list) / len(path_length_list)
        path_length_avg.append(path_length_avg_algo)

    for algo_idx in range(len(algo_names)):
        cost_avg_algo = sum(test[algo_idx] for test in cost_list) / len(cost_list)
        cost_avg.append(cost_avg_algo)

    for algo_idx in range(len(algo_names)):
        expanded_nodes_avg_algo = sum(test[algo_idx] for test in expanded_nodes_list) / len(expanded_nodes_list)
        expanded_nodes_avg.append(expanded_nodes_avg_algo)

    return path_length_avg, cost_avg, expanded_nodes_avg


def export_results_to_csv(
    path_length_avg,
    cost_avg,
    expanded_nodes_avg,
    map_size,
    start_point,
    goal_point,
    num_tests,
    filename="Task_1b_Results.csv"
):

    algorithms = [
        "Greedy (Euclidean)",
        "Greedy (Manhattan)",
        "A* (Euclidean)",
        "A* (Manhattan)",
        "Random",
        "BFS",
        "DFS",
    ]

    length_algorithms = len(algorithms)

    results = {
        "Map Width": [map_size[0]] * length_algorithms,
        "Map Height": [map_size[1]] * length_algorithms,
        "Start Point": [str(start_point)] * length_algorithms,
        "Goal Point": [str(goal_point)] * length_algorithms,
        "Number of Tests": [num_tests] * length_algorithms,
        "Algorithm": algorithms,
        "Average Path Length": path_length_avg,
        "Average Cost": cost_avg,
        "Average Expanded Nodes": expanded_nodes_avg
    }

    df = pd.DataFrame(results)

    output_path = (
        Path(__file__).resolve().parent / filename
    )

    df.to_csv(output_path, index=False)

    print(f"Results exported to: {output_path}")

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


