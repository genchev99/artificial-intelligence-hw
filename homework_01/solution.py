from functools import cached_property
from dataclasses import dataclass
from typing import Any
from collections import defaultdict
import logging

logging.basicConfig(level=logging.DEBUG)


@dataclass
class Node:
    value: Any = 'no'
    heuristic: float = 0
    color: str = 'black'


@dataclass
class Graph:
    nodes: Any
    edges: Any
    undirected_edges: Any

    def children_of(self, node_value):
        return [(self.nodes[v], w) for v, w in self.undirected_edges[node_value]]


def make_graph(nodes, edges):
    nodes = {v: Node(value=v, heuristic=h) for v, h in nodes}

    undirected_edges = defaultdict(list)
    for node, children in edges.items():
        for child, weight in children:
            undirected_edges[node].append((child, weight))
            undirected_edges[child].append((node, weight))

    return Graph(nodes=nodes, edges=edges, undirected_edges=undirected_edges)


class Turn:
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'

    def reverse(self, direction):
        if direction == Turn.left: return Turn.right
        if direction == Turn.right: return Turn.left
        if direction == Turn.up: return Turn.down
        if direction == Turn.down: return Turn.up


class Matrix:
    def __init__(self, n: int, zero_index: int, numbers: list):
        self._n = int((n + 1) ** 0.5)
        self._expected_zero_index = len(numbers) - 1 if zero_index == -1 else zero_index
        self._numbers = numbers

    def _calc_expected_index(self, number) -> int:
        if number == 0:
            return self._expected_zero_index

        if number - 1 < self._expected_zero_index:
            return number - 1

        return 0

    def _index_to_coords(self, index: int) -> tuple:
        return index // self._n, index % self._n

    def _calc_score_by_coords(self, real_coords: tuple, expected_coords: tuple) -> int:
        logging.warning(str(real_coords) + str(expected_coords))
        real_x, real_y = real_coords
        expected_x, expected_y = expected_coords

        return abs(expected_x - real_x) + abs(expected_y - real_y)

    def _get_manhattan_score(self) -> int:
        score = 0

        for index in range(len(self._numbers)):
            number = self._numbers[index]

            score_per_number = self._calc_score_by_coords(
                self._index_to_coords(index),
                self._index_to_coords(self._calc_expected_index(number)),
            )

            logging.debug(f"number: {number}, score: {score_per_number}")
            score += score_per_number

        return score

    def _get_zero_index(self) -> int:
        return self._numbers.index(0)

    def get_possible_variations(self) -> list:
        zero_x, zero_y = self._index_to_coords(self._get_zero_index())

        if zero_x > 0:


def solution(n: int, zero_index: int, table: list) -> tuple:
    """
    Finds the optimal path in a generated sequence table for `slide puzzle game`

    :return: tuple - the first member of the tuple is number of turns for the optimal
    path. The second member is list of the the turns needed to perform the optimal path.
    """

    matrix = Matrix(n=n, zero_index=zero_index, numbers=table)
    print(matrix._get_manhattan_score())


def main():
    solution(8, -1, [1, 2, 3, 5, 4, 6, 0, 7, 8])


if __name__ == '__main__':
    main()
