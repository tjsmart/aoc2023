import itertools
from typing import Literal

from lib import collect_lines
from lib import Point


def solution(s: str, factor: int = 1000000) -> int:
    universe = collect_lines(s, list)
    erows = get_expanded_rows(universe)
    ecols = get_expanded_cols(universe)
    galaxies = find_galaxies(universe)

    sum = 0
    for x, y in itertools.combinations(galaxies, 2):
        sum += compute_distance(x, y, factor, erows, ecols)

    return sum


def compute_distance(
    a: Point, b: Point, factor: int, erows: set[int], ecols: set[int]
) -> int:
    d = 0
    for x in range(a.x, b.x, sign(b.x - a.x)):
        if x in ecols:
            d += factor
        else:
            d += 1

    for y in range(a.y, b.y, sign(b.y - a.y)):
        if y in erows:
            d += factor
        else:
            d += 1

    return d


def sign(x: int) -> Literal[1, 0, -1]:
    return 1 if x > 0 else -1 if x < 0 else 1


def find_galaxies(universe: list[list[str]]) -> list[Point]:
    gs = []
    for j in range(len(universe)):
        for i in range(len(universe[0])):
            if universe[j][i] == "#":
                gs.append(Point(i, j))
    return gs


def get_expanded_rows(universe: list[list[str]]) -> set[int]:
    return {i for i, row in enumerate(universe) if "#" not in row}


def get_expanded_cols(universe: list[list[str]]) -> set[int]:
    return {
        i for i in range(len(universe[0])) if "#" not in (row[i] for row in universe)
    }


class Test:
    import pytest

    EXAMPLE_INPUT = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
    EXPECTED_RESULT = 8410

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case, factor=100) == expected
