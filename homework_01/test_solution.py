import pytest

from homework_01.solution import solution, Turn, InvalidBoardError


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


def test_solution_02():
    turns_count, turns = solution(8, -1, [2, 3, 0, 5, 1, 8, 4, 7, 6])

    assert turns_count == 16
    assert turns == [
        Turn.right,
        Turn.right,
        Turn.up,
        Turn.left,
        Turn.left,
        Turn.down,
        Turn.right,
        Turn.right,
        Turn.up,
        Turn.up,
        Turn.left,
        Turn.down,
        Turn.down,
        Turn.left,
        Turn.up,
        Turn.up,
    ]


def test_solution_03():
    turns_count, turns = solution(8, -1, [0, 5, 3, 2, 4, 6, 7, 1, 8])

    assert turns_count == 12
    assert turns == [
        Turn.up,
        Turn.left,
        Turn.up,
        Turn.right,
        Turn.down,
        Turn.left,
        Turn.down,
        Turn.right,
        Turn.up,
        Turn.up,
        Turn.left,
        Turn.left,
    ]


def test_solution_04():
    turns_count, turns = solution(8, -1, [0, 1, 5, 3, 8, 2, 7, 4, 6])

    assert turns_count == 20
    assert turns == [
        Turn.left,
        Turn.left,
        Turn.up,
        Turn.up,
        Turn.right,
        Turn.down,
        Turn.right,
        Turn.up,
        Turn.left,
        Turn.left,
        Turn.down,
        Turn.right,
        Turn.up,
        Turn.right,
        Turn.down,
        Turn.left,
        Turn.down,
        Turn.left,
        Turn.up,
        Turn.up,
    ]


def test_solution_4_by_4():
    turns_count, turns = solution(15, -1, [1, 0, 3, 4, 5, 2, 7, 8, 9, 6, 11, 12, 13, 10, 14, 15])

    assert turns_count == 5
    assert turns == [
        Turn.up,
        Turn.up,
        Turn.up,
        Turn.left,
        Turn.left,
    ]


def test_solution_should_throw_invalid_board_error():
    with pytest.raises(InvalidBoardError):
        solution(8, -1, [1, 2, 3, 4, 5, 6, 8, 0, 7])


def test_solution_4_by_4_should_throw_invalid_board_error():
    with pytest.raises(InvalidBoardError):
        solution(15, -1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0])
