
class AntColonyBasic:
    def __init__(self):
        self.pheromone_persistence_factor = 0
        self.theta = 0
        self.L = 0


class Ant:
    def __init__(self):
        print("ant")


class GreedyAnt:
    def __init__(self, capacity, home_city):
        self.capacity = capacity
        self.traveled_distance = 0
        self.current_load = capacity
        self.current_city = home_city
        self.home_city = home_city

    def load(self):
        self.current_load = self.capacity

    def reset(self, capacity, home_city):
        self.current_city = home_city
        self.current_load = capacity
        self.capacity = capacity
        self.traveled_distance = 0
        self.home_city = home_city

    def add_distance(self, distance):
        self.traveled_distance = self.traveled_distance + distance
