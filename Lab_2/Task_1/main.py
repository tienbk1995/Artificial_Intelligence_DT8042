import numpy as np
import matplotlib.pyplot as plt
from Code_Sample import path_planning as pp
import unin_random as unin_ran
import in_greedy as informed
import validation as val

def uninformed_random():
    new_map = pp.generateMap2d([60, 60])
    start, goal, path, cost = unin_ran.random_search(new_map)
    print("\n===== RANDOM SEARCH RESULTS =====")
    print(f"Path length: {len(path) - 1}")
    print(f"Total cost: {cost}")
    print(f"Number of positions: {len(path)}")
    print("\nPath:")
    for i, position in enumerate(path):
        print(f"Step {i}: {tuple(map(int, position))}")
    return (new_map, start, goal, path, cost)

if __name__ == "__main__":
    new_map, start, goal, path, cost = uninformed_random()
    val.validate_path(new_map, path, start, goal)
