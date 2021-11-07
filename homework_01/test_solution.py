from homework_01.solution import solution, Turn


def test_solution_with_provided_example():
    turns_count, turns = solution(8, -1, [1, 2, 3, 4, 5, 6, 0, 7, 8])

    assert turns_count == 2
    assert turns == [Turn.left, Turn.left]
