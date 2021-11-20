import random
import itertools

from functools import cached_property


class City:
    def __init__(self, pos_width: int, pos_height: int):
        self.pos_width = pos_width
        self.pos_height = pos_height

    def __eq__(self, other):
        return self.pos_width == other.pos_width and self.pos_height == other.pos_height

    def __ne__(self, other):
        return self.pos_width != other.pos_width or self.pos_height != other.pos_height

    def __hash__(self):
        return (self.pos_width, self.pos_height).__hash__()

    def __str__(self):
        return f"({self.pos_width}, {self.pos_height})"

    def distance(self, other):
        """
        Returns the distance to other city using pythagore
        """
        return (abs(self.pos_width - other.pos_width) ** 2 + abs(self.pos_height - other.pos_height) ** 2) ** 0.5


class Grid:
    GRID_WIDTH = 1000
    GRID_HEIGHT = 1000

    @classmethod
    def generate_random_city(cls) -> City:
        """
        Generates one city represented as tuple where the first member is the width and the second is the height
        :return:
        """
        return City(random.randrange(cls.GRID_WIDTH), random.randrange(cls.GRID_HEIGHT))

    @classmethod
    def generate_cities(cls, cities_count: int) -> set:
        """
        Generates N unique cities represented as tuples where N is equal to cities_count
        """
        cities = set()

        while len(cities) != cities_count:
            cities.add(cls.generate_random_city())

        return cities


class Route:
    def __init__(self, route: list):
        self.route = route

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return f"{str(self.fitness).zfill(22)} - {' -> '.join([str(city) for city in self.route])}"

    @cached_property
    def distance(self):
        distance = 0.0  # -_-
        for city_index in range(len(self.route) - 1):
            from_city: City = self.route[city_index]
            to_city: City = self.route[city_index + 1]

            distance += from_city.distance(to_city)

        return distance

    @cached_property
    def fitness(self):
        """
        Calculates the fitness of a route represented as a list (has order)
        """
        # Depending on the distance we return a fitness number which will be between 0 and 1
        # The more the distance the less the fitness score (we want to maximise the fitness)
        if self.distance == 0.0:
            # Edge case where the distance is equal to zero (less than 2 cities)
            return 1.0

        return 1 / self.distance

    def __add__(self, other):
        if not isinstance(other, Route):
            raise ValueError("other is not of type Route")
        # Breed
        length = len(self.route)
        cut_points = sorted([random.randrange(length), random.randrange(length)])
        cut = self.route[slice(*cut_points)]
        child = cut + [x for x in other.route if x not in cut]

        return Route(child)


class Solution:
    POPULATION_SIZE = 10
    ELITISM_SIZE = 1  # Retain top N members from the previous generation to the next one
    MAX_GENERATIONS = 10

    def __init__(self, cities_count: int):
        self.cities_count = cities_count
        self.current_generation = 0
        self.cities = Grid.generate_cities(cities_count)
        #  Create init population
        self.population = [Route(random.sample(self.cities, cities_count)) for _ in range(self.POPULATION_SIZE)]

    def __next__(self):
        """
        Returns the next generation
        """
        if self.current_generation > self.MAX_GENERATIONS:
            raise StopIteration()

        # For mating pool we'll choose 50% of most fit
        mating_pool = self.sorted_population[:self.POPULATION_SIZE // 2]
        next_generation = self.sorted_population[:self.ELITISM_SIZE]

        for _ in range(self.POPULATION_SIZE - self.ELITISM_SIZE):
            parent_a, parent_b = random.sample(mating_pool, 2)
            next_generation.append(parent_a + parent_b)

        self.population = next_generation
        self.current_generation += 1
        return self

    def __iter__(self):
        return self

    def __str__(self):
        return str(self.sorted_population[0])

    @property
    def sorted_population(self):
        return sorted(self.population, reverse=True)

    @property
    def cities_count(self):
        return self.__cities_count

    @cities_count.setter
    def cities_count(self, val: int):
        if not isinstance(val, int) or val < 0 or val > 100:
            raise ValueError("city_count cannot be below 0 or more than 100")

        self.__cities_count = val


def solution(cities_count: int):
    sol = Solution(cities_count)
    for generation in sol:
        print(generation)


def main():
    # cities_count = int(input("Input number cities: "))
    solution(cities_count=10)


if __name__ == '__main__':
    main()
