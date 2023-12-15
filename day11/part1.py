import itertools

from lib import collect_lines
from lib import Point


def solution(s: str) -> int:
    universe = collect_lines(s, list)
    expand(universe)
    galaxies = find_galaxies(universe)

    sum = 0
    for x, y in itertools.combinations(galaxies, 2):
        sum += compute_distance(x, y)

    return sum


def compute_distance(x: Point, y: Point) -> int:
    d = y - x
    return abs(d.x) + abs(d.y)


def find_galaxies(universe: list[list[str]]) -> list[Point]:
    gs = []
    for j in range(len(universe)):
        for i in range(len(universe[0])):
            if universe[j][i] == "#":
                gs.append(Point(i, j))
    return gs


def expand(universe: list[list[str]]) -> None:
    irows: list[int] = []
    for i, row in enumerate(universe):
        if "#" not in row:
            irows.append(i)

    icols = []
    for i in range(len(universe[0])):
        if "#" not in (row[i] for row in universe):
            icols.append(i)

    ner = 0
    for irow in irows:
        universe.insert(irow + ner, ["."] * len(universe[0]))
        ner += 1

    nec = 0
    for icol in icols:
        for j in range(len(universe)):
            universe[j].insert(icol + nec, ".")
        nec += 1


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
    EXPECTED_RESULT = 374

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected

    def test_expanded(self):
        universe = collect_lines(self.EXAMPLE_INPUT, list)
        expand(universe)
        assert (
            "\n".join("".join(row) for row in universe)
            == """\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#......."""
        )
