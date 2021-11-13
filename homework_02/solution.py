import random
import time


class ChessBoard:
    def __init__(self, board_size: int):
        # When know that queens cannot be on the same row. That's why our algorithm won't even bother to put them on the same row.
        # Our board of queens will be represented with a list of queens where the index and item will be the number of the row (-1) and
        # the value inside that index will be the column (-1) where the queen is positioned
        # self.__queens = list(range(board_size))
        self.__board_size = board_size
        self.__init_board()

    def __init_board(self):
        self.__queens = [0] * self.__board_size

        pos = 1
        for row in range(self.__board_size):
            self.__queens[row] = pos
            pos += 2
            if pos >= self.__board_size:
                pos = 0

    def __calculate_conflicts(self, queen_row: int, queen_col: int) -> int:
        """
        Calculates all conflicts on the board with a given queen
        """
        conflicts_count = 0

        for other_queen_row in range(len(self.__queens)):
            # If the other queen row (index) is equal to the queen_row (index) we continue because this is the same queen
            if other_queen_row == queen_row:
                continue

            other_queen_col = self.__queens[other_queen_row]

            # If they are on the same column or they are position in diagonal we increment the conflicts counter
            if self.__queens[other_queen_row] == queen_col or abs(queen_col - other_queen_col) == abs(queen_row - other_queen_row):
                conflicts_count += 1

        return conflicts_count

    def __move_queen(self, queen_row: int):
        """
        Moves queen to the column with lowest conflicts count.

        * If the queen is already on that place nothing happens
        ** If there are multiple columns where the conflicts count is minimized then a random one is picked between them
        """
        # At the beginning the min conflict is equal to the board size i.e. all queens are in conflict
        current_min_conflict = self.__board_size
        # And there are no available columns that will minimize the conflict of that queen
        columns_with_minimal_conflicts = []

        # We iterate over all columns on the board
        for other_column in range(self.__board_size):
            # If other column is equal to the current column of the queen nothing happens
            if other_column == self.__queens[queen_row]:
                continue
            # And calculate the possible conflicts count if the queen was placed there
            other_min_conflict = self.__calculate_conflicts(queen_row=queen_row, queen_col=other_column)
            if other_min_conflict < current_min_conflict:
                # If the found conflict count is less than the existing minconflict count then we want this to be our new minconflict count
                columns_with_minimal_conflicts = [other_column]
                current_min_conflict = other_min_conflict
            elif other_min_conflict == current_min_conflict:
                # If the found conflict count is equal to the existing minconflict count we want to add the new column to the list of
                # available columns that minimizes the conflicts
                columns_with_minimal_conflicts.append(other_column)

        # Finally if the list of columns that will minimize the conflicts is not empty
        if columns_with_minimal_conflicts:
            # We change the position of the queen to a randomly selected column (from the minimization list)
            self.__queens[queen_row] = random.choice(columns_with_minimal_conflicts)

    def solve(self) -> int:
        """
        Solves the board - finds a solution where all queens won't be in conflict
        """
        # This function will return the number of moves need to order the board (and also will move the queens)
        moves = 0
        while True:
            # We calculate the sum of all conflict count per queen on the board
            conflicts = 0
            queen_to_move = -1
            queen_to_move_conflicts = 0

            for queen_row in range(self.__board_size):
                conflict = self.__calculate_conflicts(queen_row, self.__queens[queen_row])
                if conflict > queen_to_move_conflicts:
                    queen_to_move_conflicts = conflict
                    queen_to_move = queen_row

                conflicts += conflict

            # If that sum is equal to 0 then all queens are "in peace" and the solution is over
            if conflicts == 0:
                # We return the count of moves needed to solve the board
                return moves

            # If the board has conflicts (not solved yet) we select a random a queen and then we move it to the position with min conflicts
            # queen_to_move = random.randint(0, self.__board_size - 1)
            self.__move_queen(queen_to_move)

            # And finally we need to increment the moves counter with one
            moves += 1

    def __str__(self):
        rows = []

        for queen_col in self.__queens:
            rows.append("_ " * queen_col + "*" + " _" * (self.__board_size - queen_col - 1))

        return "\n".join(rows)


def solution(board_width: int) -> tuple:
    chess_board = ChessBoard(board_width)

    return chess_board.solve(), str(chess_board)


def main():
    board_width = int(input("Input board width: "))

    if board_width <= 0:
        raise ValueError("The board width cannot be less than zero")

    start = time.time()
    moves, board = solution(board_width)
    end = time.time()

    # print(board)
    print("Execution time in seconds: " + "{:.2f}".format(end - start))
    print(f"Moves needed to solve the board: {moves}")


if __name__ == '__main__':
    main()
