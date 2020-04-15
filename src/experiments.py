import numpy as np
import pandas as pd
from src.data_reader import read_data
from src.ants import AntColonyBasic
from src.algorithms import GreedyAlgorithm


class Experiments:
    def __init__(self):
        self.results = []
        self.repeat_count = None
        self.greedy_algorithm = None
        self.aco_basic = None
        self.aco_swap = None
        self.aco_2_opt = None
        self.aco_swap_2_opt = None
        self.path = '../data/instances/'

    def calculate_rpd(self, optimal, best_find):
        return (best_find-optimal)/optimal * 100

    def save_results(self, path):
        df = pd.DataFrame(self.results, columns = ['exp_name', 'alg_name', 'filename', 'iterations', 'ant_number', 'capacity', 'p_factor', 'solution', 'rpd'])
        print('Writing to file....')
        df.to_csv(path)

    def run(self, repeat_count):
        self.repeat_count = repeat_count
        self.run_ants_number_exp()
        self.save_results('../ant_number_results.csv')
        self.run_iteration_exp()
        self.save_results('../iteration_results.csv')
        self.run_p_factor_exp()
        self.save_results('../p_factor_results.csv')
        self.run_cities_exp()
        self.save_results('../cities_results.csv')

    def run_cities_exp(self):
        filenames = [self.path + 'A-n32-k5.xlsx', self.path+'A-n44-k6.xlsx', self.path + 'A-n54-k7.xlsx']
        for filename in filenames:
            for i in range(0, self.repeat_count):
                print('Running cities exp for %s  %d repeat count' % (filename, i))
                self.run_algorithm('cities', filename, False, False, 1000, 3, 100, 0.8)
                self.run_algorithm('cities', filename, True, False, 1000, 3, 100, 0.8)
                self.run_algorithm('cities', filename, False, True, 1000, 3, 100, 0.8)
                self.run_algorithm('cities', filename, True, True, 1000, 3, 100, 0.8)

    def run_p_factor_exp(self):
        filenames = [self.path + 'A-n32-k5.xlsx']
        p_factors = [0.7, 0.8, 0.9]
        for filename in filenames:
            for p_factor in p_factors:
                for i in range(0, self.repeat_count):
                    print('Running p_factor exp for %s with %f p_factor %d repeat count' % (filename, p_factor, i))
                    self.run_algorithm('p_factor', filename, False, False, 1000, 3, 100, p_factor)
                    self.run_algorithm('p_factor', filename, True, False, 1000, 3, 100, p_factor)
                    self.run_algorithm('p_factor', filename, False, True, 1000, 3, 100, p_factor)
                    self.run_algorithm('p_factor', filename, True, True, 1000, 3, 100, p_factor)

    def run_iteration_exp(self):
        filenames = [self.path + 'A-n32-k5.xlsx']
        iterations = [500, 1000, 2000]
        for filename in filenames:
            for it in iterations:
                for i in range(0, self.repeat_count):
                    print('Running iteration exp for %s with %d iter %d repeat count' % (filename, it, i))
                    self.run_algorithm('iteration', filename, False, False, it, 3, 100, 0.8)
                    self.run_algorithm('iteration', filename, True, False, it, 3, 100, 0.8)
                    self.run_algorithm('iteration', filename, False, True, it, 3, 100, 0.8)
                    self.run_algorithm('iteration', filename, True, True, it, 3, 100, 0.8)

    def run_ants_number_exp(self):
        filenames = [self.path + 'A-n32-k5.xlsx']
        ant_numbers = [3, 6, 10]
        for filename in filenames:
            for ant_number in ant_numbers:
                for i in range(0, self.repeat_count):
                    print('Running ant_number exp for %s with %d ants %d repeat count' % (filename, ant_number, i))
                    self.run_algorithm('ant_number', filename, False, False, 1000, ant_number, 100, 0.8)
                    self.run_algorithm('ant_number', filename, True, False, 1000, ant_number, 100, 0.8)
                    self.run_algorithm('ant_number', filename, False, True, 1000, ant_number, 100, 0.8)
                    self.run_algorithm('ant_number', filename, True, True, 1000, ant_number, 100, 0.8)

    def run_greedy_all(self):
        filenames = [self.path + 'A-n32-k5.xlsx', self.path+'A-n44-k6.xlsx', self.path + 'A-n54-k7.xlsx']
        for filename in filenames:
            self.run_greedy('cities', filename)
        self.run_greedy('all', filenames[0])
        self.save_results('../greedy_results.csv')

    def run_greedy(self, exp_name, filename):
        instance = read_data(filename)
        greedy = GreedyAlgorithm(100, instance, 1)
        greedy.run()
        best = greedy.ant.traveled_distance
        optimal = instance.optimal_solution
        rpd = self.calculate_rpd(optimal, best)
        self.results.append([exp_name, 'greedy', filename, None, None, None, None, best, rpd])

    def run_algorithm(self, exp_name, filename, swap_enabled, _2_opt_enabled, iterations, ants_number, capacity, p_factor):
        instance = read_data(filename)
        v_count = instance.vehicles_count
        aco = AntColonyBasic(instance, ants_number=10, persistence_factor=p_factor, theta=80, alpha=2, beta=5,
                             capacity=capacity,
                             vehicle_count=v_count, best_ants_number=ants_number, iterations=iterations)
        aco.swap_enabled = swap_enabled
        aco.is_2_opt_enabled = _2_opt_enabled
        aco.run()
        best = aco.best_solution
        optimal = instance.optimal_solution
        rpd = self.calculate_rpd(optimal, best)
        print('res %d  rpd %d ' % (best, rpd))
        name = 'aco_basic'
        if swap_enabled:
            name = 'aco_swap'
        if _2_opt_enabled:
            name = 'aco_2_opt'
        if swap_enabled and _2_opt_enabled:
            name = 'aco_both'

        self.results.append([exp_name, name, filename, iterations, ants_number, capacity, p_factor, best, rpd])
