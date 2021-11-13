#include <cmath>
#include <vector>
#include <iostream>
#include <chrono>

using namespace std;

class ChessBoard {
private:
    long _board_width;
    long *_queens;

public:
    ChessBoard(long board_width) {
        this->_board_width = board_width;
        this->_queens = new long[board_width];

        int pos = 1;
        for (int row = 0; row < this->_board_width; row++) {
            this->_queens[row] = pos;
            pos += 2;
            if (pos >= this->_board_width) {
                pos = 0;
            }
        }
    }

    long _calculate_conflict(long queen_row, long queen_col) {
        long conflicts_count = 0;

        for (long row = 0; row < this->_board_width; row++) {
            if (row == queen_row) {
                continue;
            }

            long other_queen_col = this->_queens[row];

            if (row == queen_row || abs(queen_col - other_queen_col) == abs(queen_row - row)) {
                conflicts_count += 1;
            }
        }

        return conflicts_count;
    }

    void _move_queen(long queen_row) {
        long min_conflict = this->_board_width;
        vector<long> minimal_conflicts = vector<long>();

        for (long col = 0; col < this->_board_width; col++) {
            long current_conflict_count = this->_calculate_conflict(queen_row, col);

            if (current_conflict_count < min_conflict) {
                min_conflict = current_conflict_count;
                minimal_conflicts.clear();
                minimal_conflicts.push_back(col);
            } else if (current_conflict_count == min_conflict) {
                minimal_conflicts.push_back(col);
            }
        }

        if (!minimal_conflicts.empty()) {
            this->_queens[queen_row] = minimal_conflicts[random() % minimal_conflicts.size()];
        }
    }

    long solve() {
        long moves = 0;

        while (true) {
            long conflicts = 0;

            for (long row = 0; row < this->_board_width; row++) {
                conflicts += this->_calculate_conflict(row, this->_queens[row]);
            }

            if (conflicts == 0) {
                return moves;
            }

            moves += 1;
            this->_move_queen(random() % (this->_board_width));
        }
    }

    void display() {
        for (long row = 0; row < this->_board_width; row++) {
            for (long c = 0; c < this->_queens[row]; c++) {
                cout << "_ ";
            }
            cout << "* ";
            for (long c = 0; c < this->_board_width - this->_queens[row] - 1; c++) {
                cout << "_ ";
            }
            cout << endl;
        }
    }
};

int main() {
    srand(time(NULL));
    long board_width = 0;

    cout << "Input board width: ";
    cin >> board_width;

    if (board_width <= 0 || board_width == 2 || board_width == 3) {
        cerr << "Invalid board width";
        exit(1);
    }

    auto start = chrono::high_resolution_clock::now();
    ChessBoard chess_board = ChessBoard(board_width);
    chess_board.solve();
    auto end = chrono::high_resolution_clock::now();
    auto ms_int = chrono::duration_cast<chrono::milliseconds>(end - start);

    std::cout << "Execution time: " << ms_int.count() << "ms" << endl;
//    chess_board.display();

    return 0;
}
