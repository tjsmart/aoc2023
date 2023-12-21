from collections.abc import Iterator

from lib import FrozenGrid
from lib import Point


def solution(s: str, steps: int = 64) -> int:
    grid = FrozenGrid.from_str(s)
    locations = {grid.find("S")}
    for _ in range(steps):
        locations = {sp for l in locations for sp in get_steps(l, grid)}

    return len(locations)


def get_steps(l: Point, grid: FrozenGrid) -> Iterator[Point]:
    for n in l.iter_neighbors(diagonals=False):
        try:
            c = grid[n.y][n.x]
        except IndexError:
            continue

        if c != "#":
            yield n


class Test:
    import pytest

    EXAMPLE_INPUT = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
    EXPECTED_RESULT = 16

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case, steps=6) == expected
