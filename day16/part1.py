from collections import defaultdict

from lib import collect_lines
from lib import Point

type Direction = Point


def solution(s: str) -> int:
    grid = collect_lines(s, list)
    energized: dict[Point, list[Direction]] = defaultdict(list)
    queue: list[tuple[Point, Direction]] = []
    queue.append((Point(0, 0), Point(1, 0)))
    while queue:
        loc, dir = queue.pop()

        if loc.y < 0 or loc.y >= len(grid):
            continue

        if loc.x < 0 or loc.x >= len(grid[0]):
            continue

        if dir in energized[loc]:
            continue

        tile = grid[loc.y][loc.x]
        energized[loc].append(dir)
        match tile, dir:
            case (".", _) | ("-", (_, 0)) | ("|", (0, _)):
                dirs = [dir]
            case ("\\", (x, 0)):
                dirs = [(0, x)]
            case ("\\", (0, y)):
                dirs = [(y, 0)]
            case ("/", (x, 0)):
                dirs = [(0, -x)]
            case ("/", (0, y)):
                dirs = [(-y, 0)]
            case ("-", (0, y)):
                dirs = [(1, 0), (-1, 0)]
            case ("|", (x, 0)):
                dirs = [(0, 1), (0, -1)]
            case (c, _):
                assert False, f"unexpected tile: {c}"

        for dir in dirs:
            queue.append((loc + dir, Point(*dir)))

    return len(energized)


class Test:
    import pytest

    EXAMPLE_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
    EXPECTED_RESULT = 46

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
