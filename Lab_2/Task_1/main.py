import numpy as np
import matplotlib.pyplot as plt
from Code_Sample import path_planning as pp
import unin_random as unin_ran
import unin_BFS as BFS
import unin_DFS as DFS
import in_greedy as informed
import validation as val


def formatting(search_pf=False):
    path, cost = search_pf()
    print("\n===== SEARCH RESULTS =====")
    print(f"Path length: {len(path) - 1}")
    print(f"Total cost: {cost}")
    print(f"Number of positions: {len(path)}")
    print("\nPath:")
    for i, position in enumerate(path):
        print(f"Step {i}: {tuple(map(int, position))}")
    return (path, cost)

if __name__ == "__main__":
    new_map = pp.generateMap2d([60, 60])
    start_point = (np.where(new_map == -2)[0][0], np.where(new_map == -2)[1][0])
    goal_point = (np.where(new_map == -3)[0][0], np.where(new_map == -3)[1][0])

    rand_path, rand_cost = formatting(search_pf=lambda: unin_ran.randomS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, rand_path, start_point, goal_point)

    BFS_path, BFS_cost = formatting(search_pf=lambda: BFS.BFS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, BFS_path, start_point, goal_point)

    DFS_path, DFS_cost = formatting(search_pf=lambda: DFS.DFS(map=new_map, start=start_point, goal=goal_point))
    val.validate_path(new_map, DFS_path, start_point, goal_point)
