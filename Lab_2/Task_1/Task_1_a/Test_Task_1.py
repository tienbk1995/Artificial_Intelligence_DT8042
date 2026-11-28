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

all_path_length_list = []
all_cost_list = []
all_expanded_nodes_list = []

if __name__ == "__main__":

    number_of_tests = int(input("Enter the number of tests to run: "))
    plot_results_each_test = input("Do you want to plot the results each test? (y/n): ").lower()
    validate_results = input("Do you want to validate the results each test? (y/n): ").lower()
    plot_results_avg = input("Do you want to plot the average results of all tests? (y/n): ").lower()
    csv_output = input("Do you want to save the results to a CSV file? (y/n): ").lower()

    for test_num in range(number_of_tests):
        size_x, size_y = random.randint(20, 100), random.randint(20, 100)
        new_map, start_point, goal_point = main_module.init_map([size_x, size_y])

        greedy_path_euclidean, greedy_cost_euclidean, greedy_expanded_nodes_euclidean = main_module.formatting(
            search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, 
                                                   heuristic=greedy.euclidean_distance))

        greedy_path_manhattan, greedy_cost_manhattan, greedy_expanded_nodes_manhattan = main_module.formatting(
            search_pf=lambda: greedy.greedy_search(map=new_map, start=start_point, goal=goal_point, 
                                                   heuristic=greedy.manhattan_distance))

        astar_path_euclidean, astar_cost_euclidean, astar_expanded_nodes_euclidean = main_module.formatting(
            search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, 
                                                  heuristic=astar.euclidean_distance))

        astar_path_manhattan, astar_cost_manhattan, astar_expanded_nodes_manhattan = main_module.formatting(
            search_pf=lambda: astar.A_star_search(map=new_map, start=start_point, goal=goal_point, 
                                                  heuristic=astar.manhattan_distance))

        rand_path, rand_cost, rand_expanded_nodes = main_module.formatting(
            search_pf=lambda: unin_ran.randomS(map=new_map, start=start_point, goal=goal_point))

        BFS_path, BFS_cost, BFS_expanded_nodes = main_module.formatting(
            search_pf=lambda: BFS.BFS(map=new_map, start=start_point, goal=goal_point))

        DFS_path, DFS_cost, DFS_expanded_nodes = main_module.formatting(
            search_pf=lambda: DFS.DFS(map=new_map, start=start_point, goal=goal_point))

        if validate_results == "y":
            val.validate_path(new_map, greedy_path_euclidean, start_point, goal_point)
            val.validate_path(new_map, greedy_path_manhattan, start_point, goal_point)
            val.validate_path(new_map, astar_path_euclidean, start_point, goal_point)
            val.validate_path(new_map, astar_path_manhattan, start_point, goal_point)
            val.validate_path(new_map, rand_path, start_point, goal_point)
            val.validate_path(new_map, BFS_path, start_point, goal_point)
            val.validate_path(new_map, DFS_path, start_point, goal_point)

        all_path_length = [len(greedy_path_euclidean) - 1, 
                           len(greedy_path_manhattan) - 1, 
                           len(astar_path_euclidean) - 1, 
                           len(astar_path_manhattan) - 1, 
                           len(rand_path) - 1, 
                           len(BFS_path) - 1, 
                           len(DFS_path) - 1]
    
        all_cost = [greedy_cost_euclidean, 
                    greedy_cost_manhattan, 
                    astar_cost_euclidean, 
                    astar_cost_manhattan, 
                    rand_cost, 
                    BFS_cost, 
                    DFS_cost]
        
        all_expanded_nodes = [greedy_expanded_nodes_euclidean, 
                              greedy_expanded_nodes_manhattan, 
                              astar_expanded_nodes_euclidean, 
                              astar_expanded_nodes_manhattan, 
                              rand_expanded_nodes, 
                              BFS_expanded_nodes, 
                              DFS_expanded_nodes]
        
        all_path_length_list.append(all_path_length)
        all_cost_list.append(all_cost)
        all_expanded_nodes_list.append(all_expanded_nodes)
    
        if plot_results_each_test == "y":
            main_module.plot_path(new_map, greedy_path_euclidean, title_="Greedy Search with Euclidean Heuristic")
            main_module.plot_path(new_map, greedy_path_manhattan, title_="Greedy Search with Manhattan Heuristic")
            main_module.plot_path(new_map, astar_path_euclidean, title_="A* Search with Euclidean Heuristic")
            main_module.plot_path(new_map, astar_path_manhattan, title_="A* Search with Manhattan Heuristic")
            main_module.plot_path(new_map, rand_path, title_="Random Search")
            main_module.plot_path(new_map, BFS_path, title_="Breadth-First Search")
            main_module.plot_path(new_map, DFS_path, title_="Depth-First Search")

            main_module.performance(all_path_length, all_cost, all_expanded_nodes)

    # Calculate average metrics after all tests
    average_path_length, average_cost, average_expanded_nodes = main_module.calculate_performance_metrics(all_path_length_list, all_cost_list, all_expanded_nodes_list)

    if csv_output == "y":
        main_module.export_results_to_csv(average_path_length, average_cost, average_expanded_nodes, 
                                          [size_x, size_y], start_point, goal_point, number_of_tests,
                                          filename="performance_metrics_1a.csv")

    if plot_results_avg == "y":
        main_module.performance(average_path_length, average_cost, average_expanded_nodes)

