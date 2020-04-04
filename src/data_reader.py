import numpy as np
import pandas as pd


class Map:

    def __init__(self, demands, costs):
        self.costs = costs
        self.demands = demands


def read_data(path):
    coordinates = pd.read_excel(path, sheet_name='coordinates', header=None)
    number_of_targets = coordinates.shape[0]
    costs = calculate_costs(coordinates, number_of_targets)
    demands = pd.read_excel(path, sheet_name='demands', header=None)
    problem_map = Map(np.array(demands), costs)
    return problem_map


def calculate_costs(coordinates, n):
    costs = np.zeros((n, n))
    for i in range(0, n):
        for j in range(i, n):
            a = coordinates.iloc[i]
            b = coordinates.iloc[j]
            distance = np.sqrt((a[0]-b[0])**2 + (a[1] - b[1])**2)
            costs[i][j] = costs[j][i] = distance
    return costs
