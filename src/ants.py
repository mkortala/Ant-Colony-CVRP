import numpy as np


class AntColonyBasic:
    def __init__(self, world, ants_number, persistence_factor, theta, alpha, beta, capacity, vehicle_count):
        self.pheromone_persistence_factor = persistence_factor
        self.best_solution = 0
        self.ants_number = ants_number
        self.theta = theta
        self.world = world
        self.ants = []
        self.alpha = alpha
        self.beta = beta
        self.L_avg = 0
        self.capacity = capacity
        self.vehicle_count = vehicle_count

    def run(self):
        for ant in self.ants:
            if ant.can_move():
                ant.move()

    def restart(self):
        self.best_solution = 0
        self.L_avg = 0
        for ant in self.ants:
            ant.set_world(self.world, self.capacity, self.vehicle_count)

    def create_colony(self):
        for i in range(self.ants_number):
            ant = Ant(self.alpha, self.beta)
            ant.set_world(self.world, self.capacity, self.vehicle_count)
            self.ants.append(ant)

    def evaporate_pheromone(self):
        self.world.pheromones = (self.pheromone_persistence_factor + self.theta / self.L_avg) * self.world.pheromones

    def update_pheromone(self):
        delta = np.zeros(self.world.pheromones.shape)


class Ant:
    highest_id = 0

    def __init__(self, alpha, beta):
        self.id = self.__class__.highest_id
        self.__class__.highest_id += 1
        self.alpha = alpha
        self.beta = beta
        self.world = None
        self.visited = []
        self.distance = 0
        self.start = None
        self.vehicle_capacity = -1
        self.capacity_left = -1
        self.available = []
        self.first_run = True
        self.vehicles_left = 0
        self.path = []
        self.paths = []

    def set_world(self, world, capacity=100, vehicles_count=5):
        self.world = world
        self.start = np.argwhere(self.world.demands == 0)[0][0]
        self.distance = 0
        self.visited = [self.start]
        self.vehicle_capacity = self.capacity_left = capacity
        self.available = [i for i in range(self.world.city_count)]
        self.available.remove(self.start)
        self.first_run = True
        self.vehicles_left = vehicles_count
        self.path = []

    def can_move(self):
        return self.vehicles_left > 0

    def move(self):
        dest = self.choose_destination()
        self.distance += self.world.costs[self.current_city, dest]
        self.path.append((self.current_city, dest))
        self.visited.append(dest)
        self.capacity_left -= self.world.demands[dest]
        try:
            self.available.remove(dest)
        except:
            print("#%d Vehicle's going to depot" % (5 - self.vehicles_left + 1))
            self.get_new_vehicle()

    def choose_destination(self):
        if self.first_run:
            self.first_run = False
            return np.random.choice(self.available)
        available = np.array(self.available)
        available_demands = np.array([self.world.demands[i] for i in self.available])
        available = available[available_demands <= self.capacity_left]
        if len(available) == 0:
            return self.start
        d = []
        for i in available:
            d.append(1 / self.world.costs[self.current_city, i])
        probability = [np.power(self.world.pheromones[self.current_city, i], self.alpha) * np.power(
            1 / self.world.costs[self.current_city, i], self.beta) for i in available]
        prob_sum = np.divide(probability, np.sum(probability))
        s = np.sum(prob_sum)
        idx = np.argmax(prob_sum)

        return available[idx]

    def get_new_vehicle(self):
        self.vehicles_left -= 1
        self.visited = [self.start]
        self.capacity_left = self.vehicle_capacity
        self.paths.append(self.path)
        self.path = []

    @property
    def current_city(self):
        return self.visited[-1] if len(self.visited) > 0 else None


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
