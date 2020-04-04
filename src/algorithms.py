import numpy as np
from src.ants import GreedyAnt

class GreedyAlgorithm:

    def __init__(self, capacity, instance):
        self.instance = instance
        self.actual_demands = instance.demands
        self.ant = GreedyAnt(capacity, 0) #zmienic_zeby samo znajdowało
        self.cities_to_visit = np.where(self.actual_demands != 0)[0]

    def run(self):
        i = 0
        while i < 1000:
            i += 1
            closestIndex = self.findClosest()
            if closestIndex == -1:
                break
            self.moveToCity(closestIndex)

        print(self.ant.traveled_distance)

    def setWorld(self):
        print("setW")

    def restart(self, capacity, instance):
        self.ant.reset(capacity)
        self.instance = instance
        self.actual_demands = instance.demands
        self.cities_to_visit = np.where(self.actual_demands != 0)[0]

    def findClosest(self):
        if np.size(self.cities_to_visit) == 0:
            return -1
        closestIndex = self.cities_to_visit[0]
        closestValue = self.instance.costs[self.ant.current_city, self.cities_to_visit[0]]
        for x in self.cities_to_visit:
            if closestValue > self.instance.costs[self.ant.current_city, x]:
                closestIndex = x
                closestValue = self.instance.costs[self.ant.current_city, x]
        return closestIndex

    def loadAnt(self):
        self.ant.load()

    def moveToCity(self, city):
        self.addDistance(city)
        self.ant.current_city = city
        if city == self.ant.home_city:
            self.loadAnt()
        else:
            self.handleCity(city)

    def addDistance(self, city):
        self.ant.addDistance(self.instance.costs[self.ant.current_city, city])

    def handleCity(self, city):
        if self.actual_demands[city] > self.ant.current_load:
            self.actual_demands[city] = self.actual_demands[city] - self.ant.current_load
            self.ant.current_load = 0
            self.moveToCity(self.ant.home_city)
        elif self.actual_demands[city] == self.ant.current_load:
            self.actual_demands[city] = 0
            self.ant.current_load = 0
            self.cityHandled(city)
            self.moveToCity(self.ant.home_city)
        else:
            self.ant.current_load = self.ant.current_load - self.actual_demands[city]
            self.actual_demands[city] = 0
            self.cityHandled(city)

    def cityHandled(self, city):
        self.cities_to_visit = np.where(self.cities_to_visit != city)[0]


