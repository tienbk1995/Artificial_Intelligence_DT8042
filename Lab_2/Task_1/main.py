import numpy as np
import matplotlib.pyplot as plt
from Code_Sample import path_planning as pp
import unin_random as unin_ran
import Lab_2.Task_1.in_greedy as informed

def uninformed_random():
    new_map = pp.generateMap2d([60, 60])
    path, cost = unin_ran.random_search(new_map)
    print("\n===== RANDOM SEARCH RESULTS =====")
    print(f"Path length: {len(path) - 1}")
    print(f"Total cost: {cost}")
    print(f"Number of positions: {len(path)}")
    print("\nPath:")
    for i, position in enumerate(path):
        print(f"Step {i}: {tuple(map(int, position))}")

if __name__ == "__main__":
    uninformed_random()