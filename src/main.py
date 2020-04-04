from src.algorithms import GreedyAlgorithm
from src.data_reader import read_data

path = '../data_set_1.xlsx'

example_instance = read_data(path)

#print(example_instance.demands)
#print(example_instance.costs)

Greedy = GreedyAlgorithm(100, example_instance, 1)
Greedy.run()

