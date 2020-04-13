import numpy as np


class AntColonyBasic:
    def __init__(self, world, ants_number, persistence_factor, theta, alpha, beta, capacity, vehicle_count, best_ants_number, iterations=1000):
        self.pheromone_persistence_factor = persistence_factor
        self.best_solution = float('infinity')
        self.ants_number = ants_number
        self.theta = theta
        self.world = world
        self.ants = []
        self.alpha = alpha
        self.beta = beta
        self.L_avg = 0
        self.capacity = capacity
        self.vehicle_count = vehicle_count
        self.best_ants_number = best_ants_number if best_ants_number <= self.ants_number else self.ants_number
        self.iterations = iterations
        self.swap_enabled = False
        self.epsilon = .001
        self.is_2_opt_enabled = False
        self.best_path = []

    def run(self):
        self.create_colony()
        for i in range(self.iterations):
            print('Interation %d' % i)
            for ant in self.ants:
                while ant.can_move():
                    ant.move()
            if self.swap_enabled:
                self.swap()
            if self.is_2_opt_enabled:
                self.use_2_opt()

            sorted_ants = sorted(self.ants, key=lambda ant: ant.distance)
            if sorted_ants[0].distance < self.best_solution:
                self.best_solution = sorted_ants[0].distance
                self.best_path = sorted_ants[0].paths
            self.L_avg = np.average([ant.distance for ant in sorted_ants])
            self.evaporate_pheromone()
            self.update_pheromone()
            self.refresh()

    def refresh(self):
        for ant in self.ants:
            ant.set_world(self.world, self.capacity, self.vehicle_count)

    def restart(self):
        self.best_solution = 0
        self.L_avg = 0
        self.refresh()

    def create_colony(self):
        for i in range(self.ants_number):
            ant = Ant(self.alpha, self.beta)
            ant.set_world(self.world, self.capacity, self.vehicle_count)
            self.ants.append(ant)

    def evaporate_pheromone(self):
        self.world.pheromones = (self.pheromone_persistence_factor + self.theta / self.L_avg) * self.world.pheromones

    def update_pheromone(self):
        delta = np.zeros(self.world.pheromones.shape)
        sorted_ants = sorted(self.ants, key=lambda ant: ant.distance)
        for index, ant in enumerate(sorted_ants):
            if index >= self.best_ants_number:
                break
            for path in ant.paths:
                for i, city in enumerate(path):
                    if i == 0:
                        continue
                    delta[city-1, city] += (self.best_ants_number-index)/ant.distance
                    delta[city, city-1] = delta[city-1, city]
        self.world.pheromones += delta

    def swap(self):
        for ant in self.ants:
            ant.swap()

    def use_2_opt(self):
        for ant in self.ants:
            ant.use_2_opt()


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
        self.path = [self.start]
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
        self.path = [self.start]
        self.paths = []

    def can_move(self):
        return self.vehicles_left > 0

    def move(self):
        dest = self.choose_destination()
        self.distance += self.world.costs[self.current_city, dest]
        self.path.append(dest)
        self.visited.append(dest)
        self.capacity_left -= self.world.demands[dest]
        try:
            self.available.remove(dest)
        except:
            # print("#%d Vehicle's going to depot" % (5 - self.vehicles_left + 1))
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
        self.path = [self.start]

    def swap(self):
        for idx1, path1 in enumerate(self.paths):
            for idx2, path2 in enumerate(self.paths):
                if path1 == path2:
                    continue
                for index1, city1 in enumerate(path1):
                    for index2, city2 in enumerate(path2):
                        if city1 == self.start or city2 == self.start:
                            continue
                        improved, old, new = self.check_swap_improvement(path1, index1, path2, index2)
                        if improved:
                            self.make_swap(idx1, index1, idx2, index2, old, new)
                            return

    def make_swap(self, path1_index, city1_index, path2_index, city2_index, old, new):
        city1, city2 = self.paths[path1_index][city1_index], self.paths[path2_index][city2_index]
        self.paths[path1_index][city1_index] = city2
        self.paths[path2_index][city2_index] = city1
        self.distance = self.distance - old + new

    def check_swap_improvement(self, path1, city1_index, path2, city2_index):
        city1, city1_prev, city1_next = path1[city1_index], path1[city1_index-1], path1[city1_index+1]
        city2, city2_prev, city2_next = path2[city2_index], path2[city2_index-1], path2[city2_index+1]

        old_distance = self.world.costs[city1_prev, city1] + self.world.costs[city1, city1_next] + \
                       self.world.costs[city2_prev, city2] + self.world.costs[city2, city2_next]
        new_distance = self.world.costs[city1_prev, city2] + self.world.costs[city2, city1_next] + \
                       self.world.costs[city2_prev, city1] + self.world.costs[city1, city2_next]

        return new_distance < old_distance, old_distance, new_distance

    def use_2_opt(self):
        for idx, path in enumerate(self.paths):
            for i in range(1, len(path)-1):
                for j in range(i+3, len(path)-1):
                    # if path[i] == self.start or path[j] == self.start:
                    #     continue
                    improved, old, new = self.check_2_opt_improvement(path, i, j)
                    if improved:
                        self.make_2_opt_change(idx, i, j, old, new)

    def check_2_opt_improvement(self, path, i, j):
        city1, city1_prev = path[i], path[i-1]
        city2, city2_next = path[j], path[j+1]
        old_distance = self.world.costs[city1_prev, city1] + self.world.costs[city2, city2_next]
        new_distance = self.world.costs[city1_prev, city2] + self.world.costs[city1, city2_next]

        return new_distance < old_distance, old_distance, new_distance

    def make_2_opt_change(self, path_idx, city1_idx, city2_idx, old, new):
        path = self.paths[path_idx]
        middle = path[city1_idx:city2_idx+1]
        middle.reverse()
        self.paths[path_idx] = path[:city1_idx] + middle + path[city2_idx+1:]
        self.distance = self.distance - old + new

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
