import json
import math
import time
from functools import cached_property

IDA_THRESHOLD_LIMIT = 200000


class Turn:
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'


def swap(l: list, source: int, destination: int):
    l[source], l[destination] = l[destination], l[source]
    return l


class MatrixHelper:
    expected_zero_position = -1

    def __init__(self, numbers: list):
        self.__side_length = int(len(numbers) ** 0.5)
        self.__numbers = numbers

        self.__validate_board()

    def __get_expected_position_for_number(self, number) -> int:
        if number == 0:
            return self.expected_zero_position

        if number - 1 < self.expected_zero_position:
            return number - 1

        return number

    def __position_to_coords(self, index: int) -> tuple:
        return index // self.__side_length, index % self.__side_length

    def __coords_to_position(self, coords: tuple) -> int:
        x, y = coords
        return x * self.__side_length + y

    def __get_manhattan_score_by_position(self, current_position: int) -> int:
        expected_position = self.__get_expected_position_for_number(self.__numbers[current_position])

        current_x, current_y = self.__position_to_coords(current_position)
        expected_x, expected_y = self.__position_to_coords(expected_position)

        return abs(current_x - expected_x) + abs(current_y - expected_y)

    @cached_property
    def __current_zero_position(self) -> int:
        return self.__numbers.index(0)

    @cached_property
    def identifier(self) -> str:
        return "".join([str(number) for number in self.__numbers])

    @cached_property
    def manhattan_score(self) -> int:
        return sum([self.__get_manhattan_score_by_position(position) for position in range(len(self.__numbers))])

    def is_ordered(self) -> bool:
        return self.manhattan_score == 0

    def __successor_helper(self, moved_zero_position):
        order = self.__numbers.copy()
        return swap(order, self.__current_zero_position, moved_zero_position)

    def __validate_board(self):
        # TODO: implement validation
        pass

    def iter_successor(self):
        zero_x, zero_y = self.__position_to_coords(self.__current_zero_position)

        if zero_x > 0:
            yield Turn.down, self.__successor_helper(self.__coords_to_position((zero_x - 1, zero_y)))
        if zero_y > 0:
            yield Turn.right, self.__successor_helper(self.__coords_to_position((zero_x, zero_y - 1)))
        if zero_y < self.__side_length - 1:
            yield Turn.left, self.__successor_helper(self.__coords_to_position((zero_x, zero_y + 1)))
        if zero_x < self.__side_length - 1:
            yield Turn.up, self.__successor_helper(self.__coords_to_position((zero_x + 1, zero_y)))


class Node:
    def __init__(self, matrix: MatrixHelper, parent_heuristic: int = 0):
        self.matrix = matrix
        self.id = matrix.identifier
        self.heuristic = parent_heuristic + matrix.manhattan_score

    def __str__(self):
        return f"({self.id}): {self.heuristic}"

    def __eq__(self, other):
        # Make sure that other is of type Node
        if not isinstance(other, Node):
            return False

        return other.id == self.id


class Tree:
    def __init__(self, start: Node):
        self.nodes = {start.id: start}
        self.edges = {}

    def add_child(self, parent_id: str, direction: str, child: Node):
        self.nodes[child.id] = child

        if parent_id not in self.edges:
            self.edges[parent_id] = {}

        self.edges[parent_id][direction] = child.id

    def __str__(self):
        return f"Nodes: {', '.join([str(node) for key, node in self.nodes.items()])}\nEdges: {json.dumps(self.edges, indent=2)}"


class ThresholdSurpassedException(Exception):
    """
    Thrown when the threshold has been surpassed
    """
    pass


def iterative_deepening_a_star_rec(tree, node: Node, visited: set, directions: list, distance, threshold):
    if node.id in visited:
        return math.inf, directions

    if node.matrix.is_ordered():
        return -distance, directions

    estimate = distance + node.heuristic
    if estimate > threshold:
        return estimate, directions

    visited.add(node.id)

    # If not then we discover the next variations of the board and update the tree with them
    for direction, order in node.matrix.iter_successor():
        tree.add_child(parent_id=node.id, direction=direction, child=Node(MatrixHelper(order), parent_heuristic=node.heuristic))

    if not tree.edges[node.id]:
        return math.inf, directions

    min_distance = math.inf
    min_directions = []
    for direction, child_id in tree.edges[node.id].items():
        if child_id in visited:
            continue

        new_distance, new_directions = iterative_deepening_a_star_rec(
            tree=tree,
            node=tree.nodes[child_id],
            visited=visited,
            directions=[*directions, direction],
            distance=distance + 1,
            threshold=threshold,
        )

        if new_distance < min_distance:
            min_distance = new_distance
            min_directions = new_directions

    return min_distance, min_directions


def iterative_deepening_a_star(tree: Tree, start: Node):
    threshold = start.heuristic

    while True:
        distance, directions = iterative_deepening_a_star_rec(
            tree,
            start,
            visited=set(),
            directions=[],
            distance=0,
            threshold=threshold
        )

        if distance <= 0:
            return -distance, directions
        elif 0 < distance < IDA_THRESHOLD_LIMIT:
            # prevents stucking on unsolvable puzzles
            threshold = distance
        else:
            return -1, []


def solution(n: int, expected_zero_index: int, numbers: list) -> tuple:
    """
    Finds the optimal path in a generated sequence table for `slide puzzle game`

    :return: tuple - the first member of the tuple is number of turns for the optimal
    path. The second member is list of the the turns needed to perform the optimal path.
    """
    # Set the expected zero position as class attribute of MatrixHelper
    MatrixHelper.expected_zero_position = len(numbers) - 1 if expected_zero_index == -1 else expected_zero_index

    # init tree
    matrix = MatrixHelper(numbers)
    start = Node(matrix)
    tree = Tree(start)
    return iterative_deepening_a_star(tree, start)


def main():
    n = int(input("Input N: "))
    i = int(input("Input I: "))
    numbers = []
    for row_number in range(int((n + 1) ** 0.5)):
        row = input(f"Input row #{row_number + 1} separated with spaces: ")
        numbers += [int(number) for number in str(row).split(" ")]

    start = time.time()
    distance, directions = solution(n, i, numbers)
    end = time.time()
    # print the expected output
    print(distance)
    for index, direction in enumerate(directions):
        print(index, direction)

    print("Execution time in seconds: " + "{:.2f}".format(end - start))


if __name__ == '__main__':
    main()
