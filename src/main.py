from src.algorithms import GreedyAlgorithm
from src.data_reader import read_data
from src.ants import Ant
import numpy as np


path = '../data_set_1.xlsx'

example_instance = read_data(path)

print(example_instance.demands.shape)
# print(example_instance.costs)

ant = Ant(2, 2)
ant.set_world(example_instance, 100, 5)

while ant.can_move():
    ant.move()

print(ant.distance)
print('Route:')
i = 1
for path in ant.paths:
    print('Path %d' % i)
    i += 1
    for edge in path:
        print('%d ->' % edge[0], end=" ")
        if edge[1] == 0:
            print('%d' % edge[1])

# Greedy
# Greedy = GreedyAlgorithm(100, example_instance, 1)
# Greedy.run()

