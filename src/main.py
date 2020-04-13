from src.algorithms import GreedyAlgorithm
from src.data_reader import read_data
from src.ants import Ant, AntColonyBasic
import numpy as np


path = '../data_set_1.xlsx'

example_instance = read_data(path)

# print(example_instance.costs)
# Ant
# ant = Ant(2, 2)
# ant.set_world(example_instance, 100, 5)
#
# while ant.can_move():
#     ant.move()
#
# print(ant.distance)
# print('Route:')
# i = 1
# for path in ant.paths:
#     print()
#     print('Path %d' % i)
#     i += 1
#     for edge in path:
#         print(edge, end=' ')
#
# print()
# print('Po 2-opt')
# ant.use_2_opt()
# print(ant.distance)
# print('Route:')
# i = 1
# for path in ant.paths:
#     print()
#     print('Path %d' % i)
#     i += 1
#     for edge in path:
#         print(edge, end=' ')

# ACO
aco = AntColonyBasic(example_instance, ants_number=10, persistence_factor=0.8, theta=80, alpha=2, beta=5, capacity=100,
                     vehicle_count=5, best_ants_number=3, iterations=1000)
# aco.swap_enabled = True
aco.is_2_opt_enabled = True
aco.run()
print(aco.best_solution)
rpd = (aco.best_solution - 784)/784 * 100
print(rpd)

# Greedy
# Greedy = GreedyAlgorithm(100, example_instance, 1)
# Greedy.run()


