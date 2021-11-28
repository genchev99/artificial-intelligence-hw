from copy import deepcopy
from functools import cached_property
from typing import Generator


class Player:
    empty = "."
    x = "X"
    o = "O"

    @classmethod
    def revert(cls, player):
        if player == cls.x:
            return cls.o
        elif player == cls.o:
            return cls.x


class TicTacToe:
    def __init__(self, on_turn: str, matrix=None):
        self.on_turn = on_turn
        self.size = 3
        self.matrix = matrix or [[Player.empty for _ in range(self.size)] for _ in range(self.size)]

    @property
    def on_turn(self):
        return self.__on_turn

    @on_turn.setter
    def on_turn(self, val):
        if val not in [Player.x, Player.o]:
            raise ValueError(f"On turn should be either {Player.x} or {Player.o}")

        self.__on_turn = val

    @cached_property
    def streak(self) -> list:
        return [[Player.x for _ in range(self.size)], [Player.o for _ in range(self.size)]]

    def get_matrix_column(self, col):
        return [row[col] for row in self.matrix]

    def is_tie(self):
        for row in self.matrix:
            if Player.empty in row:
                return False

        return True

    @property
    def level(self):
        count = 0
        for row in self.matrix:
            count += sum([1 for x in row if not x == Player.empty])

        return count

    @property
    def score(self):
        return (self.size ** 2) + 1 - self.level

    @property
    def primary_diagonal(self) -> list:
        return [self.matrix[i][i] for i in range(self.size)]

    @property
    def secondary_diagonal(self) -> list:
        return [self.matrix[i][-i - 1] for i in range(self.size)]

    @property
    def is_over(self):
        return self.is_tie() or self.is_player_winning(Player.x) or self.is_player_winning(Player.o)

    def is_player_winning(self, player: str):
        comb = [player for _ in range(self.size)]

        for row in self.matrix:
            if row == comb:
                return True

        for col in range(self.size):
            if self.get_matrix_column(col) == comb:
                return True

        if self.primary_diagonal == comb or self.secondary_diagonal == comb:
            return True

        return False

    def is_position_valid(self, row: int, col: int):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_position_free(self, row: int, col: int):
        if not self.is_position_valid(row, col):
            raise AttributeError("Invalid coords out of range")

        return self.matrix[row][col] == Player.empty

    def mark_position(self, row: int, col: int):
        if not self.is_position_free(row, col):
            raise AttributeError("The spot is not free")

        self.matrix[row][col] = self.on_turn

    def next_player(self):
        self.on_turn = Player.revert(self.on_turn)

    def iter_possible_alternations(self) -> Generator[list, None, None]:
        for row_i in range(self.size):
            for col_i in range(self.size):
                if self.matrix[row_i][col_i] == Player.empty:
                    cp = deepcopy(self.matrix)
                    cp[row_i][col_i] = self.on_turn

                    yield cp

    def display(self):
        print("===================")
        for row in self.matrix:
            print(row)

    def display_result(self):
        if self.is_player_winning(Player.x):
            print("Player X wins")
        elif self.is_player_winning(Player.o):
            print("Player O wins")
        elif self.is_tie():
            print("TIE!")

        self.display()


def mm_max(board: TicTacToe, alpha, beta):
    if board.is_player_winning(Player.x):
        return -board.score, board.matrix

    if board.is_player_winning(Player.o):
        return board.score, board.matrix

    if board.is_tie():
        return 0, board.matrix

    max_value = float("-inf")
    alt = board.matrix

    for alternation in board.iter_possible_alternations():
        alternation_board = TicTacToe(Player.revert(board.on_turn), alternation)
        # alternation_board.display()
        res, _ = mm_min(alternation_board, alpha, beta)
        if res > max_value:
            max_value = res
            alt = alternation

        if max_value > beta:
            break

        if max_value > alpha:
            alpha = max_value

    return max_value, alt


def mm_min(board: TicTacToe, alpha, beta):
    if board.is_player_winning(Player.x):
        return -board.score, board.matrix

    if board.is_player_winning(Player.o):
        return board.score, board.matrix

    if board.is_tie():
        return 0, board.matrix

    min_value = float("inf")
    alt = board.matrix

    for alternation in board.iter_possible_alternations():
        alternation_board = TicTacToe(Player.revert(board.on_turn), alternation)
        # alternation_board.display()
        res, _ = mm_max(alternation_board, alpha, beta)
        if res < min_value:
            min_value = res
            alt = alternation

        if min_value <= alpha:
            break

        if min_value < beta:
            beta = min_value

    return min_value, alt


def game_loop(on_turn: str):
    """
    The user will be with X and the computer with O
    :param on_turn:
    :return:
    """
    tic_tac_toe = TicTacToe(on_turn)

    while not tic_tac_toe.is_over:
        tic_tac_toe.display()

        if tic_tac_toe.on_turn == Player.x:
            while True:
                raw_input = input("Input coords for X (two numbers separated with ,): ")
                row, col = [int(x) - 1 for x in raw_input.split(",")]

                if not tic_tac_toe.is_position_valid(row, col):
                    print("Invalid position coords out of range")
                    continue

                if not tic_tac_toe.is_position_free(row, col):
                    print("The position wasn't free")
                    continue

                tic_tac_toe.mark_position(row, col)
                break
        else:
            _, alt = mm_max(tic_tac_toe, float("-inf"), float("inf"))
            tic_tac_toe.matrix = alt

        tic_tac_toe.next_player()

    tic_tac_toe.display_result()


def solution():
    on_turn = input("Who should go first X (you) or O (the terminator): ")
    game_loop(on_turn)


def main():
    solution()


if __name__ == '__main__':
    main()
