from homework_01.solution import solution, Turn


def test_solution_with_provided_example():
    turns_count, turns = solution(8, -1, [1, 2, 3, 4, 5, 6, 0, 7, 8])

    assert turns_count == 2
    assert turns == [Turn.left, Turn.left]


def test_solution_already_ordered():
    turns_count, turns = solution(8, -1, [1, 2, 3, 4, 5, 6, 7, 8, 0])

    assert turns_count == 0
    assert turns == []


def test_solution_one_left_move():
    turns_count, turns = solution(8, -1, [1, 2, 3, 4, 5, 6, 7, 0, 8])

    assert turns_count == 1
    assert turns == [Turn.left]


def test_solution_one_up_move():
    turns_count, turns = solution(8, -1, [1, 2, 3, 4, 5, 0, 7, 8, 6])

    assert turns_count == 1
    assert turns == [Turn.up]


def test_solution_01():
    turns_count, turns = solution(8, -1, [0, 1, 3, 4, 2, 5, 7, 8, 6])

    assert turns_count == 4
    assert turns == [Turn.left, Turn.up, Turn.left, Turn.up]
