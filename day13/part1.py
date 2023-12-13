from lib import collect_block_lines


def solution(s: str) -> int:
    grids = collect_block_lines(s, list)
    return sum(map(calc, grids))


def calc(grid: list[list[str]]) -> int:
    if row := find_horizontal_reflection(grid):
        return 100 * row

    if col := find_vertical_reflection(grid):
        return col

    assert False, "uh oh!"


def find_horizontal_reflection(grid: list[list[str]]) -> int:
    for row in range(1, len(grid)):
        if all(
            grid[i] == grid[j]
            for i, j in zip(range(row - 1, -1, -1), range(row, len(grid), 1))
        ):
            return row
    return 0


def find_vertical_reflection(grid: list[list[str]]) -> int:
    for col in range(1, len(grid[0])):
        if all(
            grid[y][i] == grid[y][j]
            for i, j in zip(range(col - 1, -1, -1), range(col, len(grid[0]), 1))
            for y in range(len(grid))
        ):
            return col
    return 0


class Test:
    import pytest

    EXAMPLE_INPUT = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    EXPECTED_RESULT = 405

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
