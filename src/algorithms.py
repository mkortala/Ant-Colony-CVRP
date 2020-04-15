import numpy as np
from src.ants import GreedyAnt


class GreedyAlgorithm:

    def __init__(self, capacity, instance, number_of_ants):
        self.instance = instance
        self.actual_demands = instance.demands
        self.ant = GreedyAnt(capacity, np.where(instance.demands == 0)[0][0])
        self.cities_to_visit = np.where(instance.demands != 0)[0]

    def run(self):
        while self.cities_to_visit.size > 0:
            closest_city = self.find_closest()
            if closest_city == -1:
                self.move_to_city(self.ant.home_city)
            else:
                self.move_to_city(closest_city)
        # print(self.ant.traveled_distance)

    def reset(self, capacity, instance, number_of_ants):
        self.ant.reset(capacity, np.where(instance.demands == 0)[0][0])
        self.instance = instance
        self.actual_demands = instance.demands
        self.cities_to_visit = np.where(instance.demands != 0)[0]

    def find_closest(self):
        closest_city = -1
        closest_value = -1
        for x in self.cities_to_visit:
            if x != self.ant.current_city and self.actual_demands[x] <= self.ant.current_load:
                if closest_value > self.instance.costs[self.ant.current_city, x] or closest_value == -1:
                    closest_city = x
                    closest_value = self.instance.costs[self.ant.current_city, x]
        return closest_city

    def load_ant(self):
        self.ant.load()

    def move_to_city(self, city):
        self.add_distance(city)
        self.ant.current_city = city
        if city == self.ant.home_city:
            self.load_ant()
        else:
            self.handle_city(city)

    def add_distance(self, city):
        self.ant.add_distance(self.instance.costs[self.ant.current_city, city])

    def handle_city(self, city):
        if self.actual_demands[city] > self.ant.current_load:
            self.actual_demands[city] = self.actual_demands[city] - self.ant.current_load
            self.ant.current_load = 0
            self.move_to_city(self.ant.home_city)
        elif self.actual_demands[city] == self.ant.current_load:
            self.actual_demands[city] = 0
            self.ant.current_load = 0
            self.city_handled(city)
            self.move_to_city(self.ant.home_city)
        else:
            self.ant.current_load = self.ant.current_load - self.actual_demands[city]
            self.actual_demands[city] = 0
            self.city_handled(city)

    def city_handled(self, city):
        index_of_city = np.where(self.cities_to_visit == city)[0][0]
        self.cities_to_visit = np.delete(self.cities_to_visit, index_of_city)
