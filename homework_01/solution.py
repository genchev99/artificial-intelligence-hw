import json
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.CRITICAL)


class Turn:
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'


class Matrix:
    def __init__(self, n: int, zero_index: int, numbers: list):
        self._n = int((n + 1) ** 0.5)
        self._expected_zero_index = self._index_to_coords(
            len(numbers) - 1 if zero_index == -1 else zero_index)

        matrix = []
        for rows in range(self._n):
            matrix.append(numbers[rows * self._n: (rows + 1) * self._n])

        self._matrix = matrix

    def _calc_expected_index(self, number) -> tuple:
        if number == 0:
            return self._expected_zero_index

        if number - 1 < self._coords_to_index(self._expected_zero_index):
            return self._index_to_coords(number - 1)

        return self._index_to_coords(number)

    def _index_to_coords(self, index: int) -> tuple:
        return index // self._n, index % self._n

    def _coords_to_index(self, coords: tuple) -> int:
        x, y = coords
        return x * self._n + y

    def _calc_score_by_coords(self, real_coords: tuple, expected_coords: tuple) -> int:
        logging.warning(str(real_coords) + str(expected_coords))
        real_x, real_y = real_coords
        expected_x, expected_y = expected_coords

        return abs(expected_x - real_x) + abs(expected_y - real_y)

    def _get_current_zero_coords(self) -> tuple:
        for row in range(self._n):
            for col in range(self._n):
                if self._matrix[row][col] == 0:
                    return row, col

    def _as_list(self) -> list:
        res = []

        for row in self._matrix:
            res += row

        return res

    def _from_new_zero_coords(self, current_order: list, old_zero_coords: tuple, new_zero_coords: tuple) -> list:
        old_zero_index = self._coords_to_index(old_zero_coords)
        new_zero_index = self._coords_to_index(new_zero_coords)

        temp = current_order[old_zero_index]
        current_order[old_zero_index] = current_order[new_zero_index]
        current_order[new_zero_index] = temp

        return current_order

    def iter_possible_variations(self) -> list:
        zero_x, zero_y = self._get_current_zero_coords()
        current_order = self._as_list()

        if zero_x > 0:
            direction = Turn.down
            order = self._from_new_zero_coords(
                current_order=current_order.copy(),
                old_zero_coords=(zero_x, zero_y),
                new_zero_coords=(zero_x - 1, zero_y)
            )

            yield direction, order

        if zero_y > 0:
            direction = Turn.right
            order = self._from_new_zero_coords(
                current_order=current_order.copy(),
                old_zero_coords=(zero_x, zero_y),
                new_zero_coords=(zero_x, zero_y - 1)
            )

            yield direction, order

        if zero_y < self._n - 1:
            direction = Turn.left
            order = self._from_new_zero_coords(
                current_order=current_order.copy(),
                old_zero_coords=(zero_x, zero_y),
                new_zero_coords=(zero_x, zero_y + 1)
            )

            yield direction, order

        if zero_x < self._n - 1:
            direction = Turn.up
            order = self._from_new_zero_coords(
                current_order=current_order.copy(),
                old_zero_coords=(zero_x, zero_y),
                new_zero_coords=(zero_x + 1, zero_y)
            )

            yield direction, order

    def get_identifier(self) -> str:
        return "".join([str(l) for l in self._as_list()])

    def get_manhattan_score(self) -> int:
        score = 0

        for row in range(self._n):
            for col in range(self._n):
                number = self._matrix[row][col]

                score_per_number = self._calc_score_by_coords(
                    (row, col),
                    self._calc_expected_index(number),
                )

                logging.debug(f"number: {number}, score: {score_per_number}")
                score += score_per_number

        return score

    def is_solved(self) -> bool:
        return self.get_manhattan_score() == 0


@dataclass
class Node:
    def __init__(self, identifier: str, heuristic: int, matrix: Matrix):
        self.identifier = identifier
        self.heuristic = heuristic
        self.matrix = matrix


@dataclass
class Graph:
    def __init__(self, start: Node):
        self.start = start
        self.nodes = {
            start.identifier: start,
        }
        self.edges = {}
        self.reversed_edges = {}

    def display(self):
        print("nodes: ", self.nodes)
        print(json.dumps(self.edges, indent=2))

    def add_new_turn(self, from_node: str, direction: str, node: Node):
        self.nodes[node.identifier] = None

        if from_node not in self.edges:
            self.edges[from_node] = {}

        self.edges[from_node][direction] = node.identifier

        # reverse edges
        if node.identifier not in self.reversed_edges:
            self.reversed_edges[node.identifier] = {}

    def traverse_back(self, node_id: str):
        pass


def recursive_helper(n, zero_index, numbers, start_node: Node, graph, path, direction, threshold):
    if start_node.matrix.get_manhattan_score() == 0:
        return [*path, direction]

    if start_node.heuristic > threshold:
        return

    child_nodes = []
    for direction, order in start_node.matrix.iter_possible_variations():
        new_matrix = Matrix(n, zero_index, order)
        new_node = Node(new_matrix.get_identifier(), heuristic=new_matrix.get_manhattan_score() + start_node.heuristic, matrix=new_matrix)
        child_nodes.append(new_node)

        graph.add_new_turn(start_node.identifier, direction, new_node)

    # TODO: finish


def helper(n: int, zero_index: int, numbers: list):
    threshold = 0
    matrix = Matrix(n=n, zero_index=zero_index, numbers=numbers)
    start_node = Node(matrix.get_identifier(), heuristic=matrix.get_manhattan_score(), matrix=matrix)
    graph = Graph(start_node)

    while True:
        stack = [start_node]

        while stack:
            head = stack.pop()

            if head.matrix.get_manhattan_score() == 0:
                return head, graph

            if head.heuristic > threshold:
                break

            for direction, order in head.matrix.iter_possible_variations():
                new_matrix = Matrix(n, zero_index, order)
                new_node = Node(new_matrix.get_identifier(), heuristic=new_matrix.get_manhattan_score() + head.heuristic, matrix=new_matrix)

                graph.add_new_turn(head.identifier, direction, new_node)
                stack.append(new_node)

        threshold += 1


def solution(n: int, zero_index: int, numbers: list) -> tuple:
    """
    Finds the optimal path in a generated sequence table for `slide puzzle game`

    :return: tuple - the first member of the tuple is number of turns for the optimal
    path. The second member is list of the the turns needed to perform the optimal path.
    """
    leaf, graph = helper(n, zero_index, numbers)
    graph.display()


def main():
    print(solution(8, -1, [1, 2, 3, 4, 5, 6, 0, 7, 8]))


if __name__ == '__main__':
    main()
