import numpy as np
import pandas as pd


class Map:

    def __init__(self, demands, costs, vehicles_count, optimal_result):
        self.costs = costs
        self.demands = demands.reshape(demands.shape[0],)
        self.pheromones = (np.ones(self.costs.shape) - np.eye(len(self.demands)))*0.5
        self.city_count = len(self.demands)
        self.u = np.zeros(self.costs.shape)
        self.start = np.argwhere(self.demands == 0)[0][0]
        self.optimal_solution = optimal_result
        self.vehicles_count= vehicles_count
        for i in range(0,self.costs.shape[0]):
            for j in range(i, self.costs.shape[1]):
                self.u[i, j] = self.u[j, i] = self.costs[i, self.start] + self.costs[self.start, j] - self.costs[i, j]


def read_data(path):
    coordinates = pd.read_excel(path, sheet_name='coordinates', header=None)
    number_of_targets = coordinates.shape[0]
    costs = calculate_costs(coordinates, number_of_targets)
    demands = pd.read_excel(path, sheet_name='demands', header=None)
    infos = pd.read_excel(path, sheet_name='info')
    problem_map = Map(np.array(demands), costs, infos['Vehicles'][0], infos['Optimal'][0])
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

