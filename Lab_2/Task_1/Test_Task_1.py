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
    

if __name__ == "__main__":
    size_x, size_y = random.randint(20, 100), random.randint(20, 100)
    new_map, start_point, goal_point = init_map([size_x, size_y])

    greedy_path_euclidean, greedy_cost_euclidean, greedy_expanded_nodes_euclidean = formatting(search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, heuristic=greedy.euclidean_distance))
    val.validate_path(new_map, greedy_path_euclidean, start_point, goal_point)
    plot_path(new_map, greedy_path_euclidean, title_="Greedy Search with Euclidean Heuristic")

    greedy_path_manhattan, greedy_cost_manhattan, greedy_expanded_nodes_manhattan = formatting(search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, heuristic=greedy.manhattan_distance))
    val.validate_path(new_map, greedy_path_manhattan, start_point, goal_point)
    plot_path(new_map, greedy_path_manhattan, title_="Greedy Search with Manhattan Heuristic")

    astar_path_euclidean, astar_cost_euclidean, astar_expanded_nodes_euclidean = formatting(search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, heuristic=astar.euclidean_distance))
    val.validate_path(new_map, astar_path_euclidean, start_point, goal_point)
    plot_path(new_map, astar_path_euclidean, title_="A* Search with Euclidean Heuristic")

    astar_path_manhattan, astar_cost_manhattan, astar_expanded_nodes_manhattan = formatting(search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, heuristic=astar.manhattan_distance))
    val.validate_path(new_map, astar_path_manhattan, start_point, goal_point)
    plot_path(new_map, astar_path_manhattan, title_="A* Search with Manhattan Heuristic")

    rand_path, rand_cost, rand_expanded_nodes = formatting(search_pf=lambda: unin_ran.randomS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, rand_path, start_point, goal_point)
    plot_path(new_map, rand_path, title_="Random Search")

    BFS_path, BFS_cost, BFS_expanded_nodes = formatting(search_pf=lambda: BFS.BFS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, BFS_path, start_point, goal_point)
    plot_path(new_map, BFS_path, title_="Breadth-First Search")

    DFS_path, DFS_cost, DFS_expanded_nodes = formatting(search_pf=lambda: DFS.DFS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, DFS_path, start_point, goal_point)
    plot_path(new_map, DFS_path, title_="Depth-First Search")

    all_path_length = [len(greedy_path_euclidean) - 1, len(greedy_path_manhattan) - 1, len(astar_path_euclidean) - 1, len(astar_path_manhattan) - 1, len(rand_path) - 1, len(BFS_path) - 1, len(DFS_path) - 1]
    all_cost = [greedy_cost_euclidean, greedy_cost_manhattan, astar_cost_euclidean, astar_cost_manhattan, rand_cost, BFS_cost, DFS_cost]
    all_expanded_nodes = [greedy_expanded_nodes_euclidean, greedy_expanded_nodes_manhattan, astar_expanded_nodes_euclidean, astar_expanded_nodes_manhattan, rand_expanded_nodes, BFS_expanded_nodes, DFS_expanded_nodes]
    performance(all_path_length, all_cost, all_expanded_nodes)


