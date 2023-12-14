from typing import Iterator

from lib import collect_lines


def solution(s: str) -> int:
    grid = collect_lines(s, list)
    t = 0
    for col in iter_cols(grid):
        count = len(col)
        for i, c in enumerate(col):
            if c == "O":
                t += count
                count -= 1
            elif c == "#":
                count = len(col) - i - 1

    return t


def iter_cols(grid: list[list[str]]) -> Iterator[list[str]]:
    for x in range(len(grid[0])):
        yield [grid[y][x] for y in range(len(grid))]


class Test:
    import pytest

    EXAMPLE_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    EXPECTED_RESULT = 136

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
