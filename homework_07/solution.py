import argparse
import csv
import os
import pathlib
import random
from operator import itemgetter

import matplotlib.pyplot as plt

NORMAL = "normal"
UNBALANCE = "unbalance"
DELIMITERS = {
    NORMAL: "\t",
    UNBALANCE: " ",
}


def read_data(dataset: str) -> list:
    with open(os.path.join(pathlib.Path(__file__).parent.resolve(), "data", dataset, "data.txt"), "r") as fd:
        reader = csv.reader(fd, delimiter=DELIMITERS[dataset])

        return [(float(x), float(y)) for x, y in reader]


def plot(centroids: list, file: str = "plot.png"):
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    plt.xlabel('x')
    plt.ylabel('y')

    for i, centroid in enumerate(centroids):
        # plot the centers
        center_x, center_y = centroid.center
        plt.scatter(center_x, center_y, c="#000", marker="x", zorder=10)

        # plot the rest of the points
        x, y = zip(*centroid.points)
        plt.scatter(x, y, c=colors[i])

    plt.savefig(os.path.join(pathlib.Path(__file__).parent.resolve(), "plot.png"), dpi=300)


def distance(a: tuple, b: tuple) -> float:
    a_x, a_y = a
    b_x, b_y = b

    return ((a_x - b_x) ** 2 + (a_y - b_y) ** 2) ** 0.5


class Centroid:
    def __init__(self, center: tuple):
        self.center = center
        self.points = []

    def clear_points(self):
        self.points = []

    def add_point(self, point: tuple):
        self.points.append(point)

    def new_center(self):
        if not self.points:
            return self.center

        x, y = zip(*self.points)

        return sum(x) / len(x), sum(y) / len(y)

    def fit_center(self):
        self.center = self.new_center()

    def average_distance(self):
        if not self.points:
            return 0

        distances = [distance(point, self.center) for point in self.points]
        return sum(distances) / len(distances)


def should_stop(centroids: list):
    for centroid in centroids:
        if centroid.center != centroid.new_center():
            return False

    return True


def average_centroids_distance(centroids: list) -> float:
    average_distances = [centroid.average_distance() for centroid in centroids]

    return sum(average_distances) / len(average_distances)


def centroids_distances_score(centroids: list) -> float:
    total_distance = 0

    for centroid in centroids:
        for other_centroid in centroids:
            total_distance += distance(centroid.center, other_centroid.center)

    return 1 / total_distance


def average_score(centroids: list) -> float:
    return average_centroids_distance(centroids)
    # return centroids_distances_score(centroids)


def k_means(data: list, clusters_amount: int, max_iterations: int = 100) -> list:
    # initially we pick random points to be centroids
    centroids = [Centroid(centroid_coords) for centroid_coords in random.sample(data, clusters_amount)]

    for iteration in range(max_iterations):
        print("iteration: ", iteration)
        # classify the points
        for point in data:
            centroid, _ = min(zip(centroids, [distance(centroid.center, point) for centroid in centroids]), key=itemgetter(1))
            centroid.add_point(point)

        if should_stop(centroids):
            return centroids

        for centroid in centroids:
            centroid.fit_center()
            centroid.clear_points()

    return centroids


def solution(dataset: str, clusters_amount: int, random_restart_times: int = 10):
    data = read_data(dataset)
    centroids = k_means(data, clusters_amount=clusters_amount)
    best_score = average_score(centroids)

    for _ in range(random_restart_times):
        new_centroids = k_means(data, clusters_amount=clusters_amount)
        if average_score(new_centroids) < best_score:
            centroids = new_centroids

    plot(centroids)


def check_positive(val: str) -> int:
    ival = int(val)
    if ival <= 0:
        raise argparse.ArgumentTypeError(f"{val} is invalid positive int value")

    return ival


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clusters", help="Amount of clusters to find", required=True, type=check_positive)
    parser.add_argument("--dataset", help="Which dataset to use", required=True, choices=[NORMAL, UNBALANCE])
    args = parser.parse_args()

    solution(dataset=args.dataset, clusters_amount=args.clusters)


if __name__ == '__main__':
    main()
