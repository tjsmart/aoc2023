import string
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from typing import Iterator

from lib import collect_lines
from lib import Point
from lib import product


@dataclass
class Number:
    points: list[Point] = field(default_factory=list)
    chars: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.points)

    def __index__(self) -> int:
        return int("".join(self.chars))


def solution(s: str) -> int:
    grid = collect_lines(s, list)

    gear_candidates: dict[Point, list[int]] = defaultdict(list)
    for y, row in enumerate(grid):
        number = Number()
        for x, c in enumerate(row):
            if c in string.digits:
                number.points.append(Point(x, y))
                number.chars.append(c)

            else:
                if number:
                    for gear in iter_gears(number.points, grid):
                        gear_candidates[gear].append(int(number))

                number = Number()

        if number:
            for gear in iter_gears(number.points, grid):
                gear_candidates[gear].append(int(number))

    return sum(
        product(numbers) for numbers in gear_candidates.values() if len(numbers) == 2
    )


def iter_gears(points: list[Point], grid: list[list[str]]) -> Iterator[Point]:
    for n in iter_neighbors(points, grid):
        if grid[n.y][n.x] == "*":
            yield n


def iter_neighbors(points: list[Point], grid: list[list[str]]) -> Iterator[Point]:
    if points[0].y > 0:
        for x in range(points[0].x - 1, points[-1].x + 2):
            if 0 <= x < len(grid[0]):
                yield Point(x, points[0].y - 1)

    if points[0].x - 1 >= 0:
        yield Point(points[0].x - 1, points[0].y)

    if points[-1].x + 1 < len(grid[0]):
        yield Point(points[-1].x + 1, points[0].y)

    if points[0].y < len(grid) - 1:
        for x in range(points[0].x - 1, points[-1].x + 2):
            if 0 <= x < len(grid[0]):
                yield Point(x, points[0].y + 1)


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""",
                467835,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
