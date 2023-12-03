from dataclasses import dataclass
from typing import Self

from lib import Point


@dataclass
class Grid:
    value: list[list[str]]

    @classmethod
    def from_str(cls, s) -> Self:
        return Grid([list(line) for line in s.splitlines()])


def solution(s: str) -> int:
    grid = Grid.from_str(s).value
    ngroups: list[list[Point]] = []
    gears: list[Point] = []


    for j in range(len(grid)):
        for i in range(len(grid[0])):
            point = Point(i, j)
            c = grid[j][i]

            if c.isnumeric():
                if ngroups and immediately_follows(ngroups[-1], point):
                    ngroups[-1].append(point)
                else:
                    ngroups.append([point])
            elif c == '*':
                gears.append(point)

    # nothing confusing going on here at all....
    true_gears: list[list[list[Point]]] = []
    for gear in gears:
        hits: list[list[Point]] = []
        for ngroup in ngroups:
            if any(point.is_adjacent_to(gear) for point in ngroup):
                hits.append(ngroup)


        if len(hits) == 2:
            true_gears.append(hits)

    return sum(map(lambda gear: calculate_gear_ratio(gear, grid), true_gears))


def immediately_follows(ngroup: list[Point], point: Point) -> bool:
    # assume we only need to check if point is immediately to the right of previous point
    return point.x == ngroup[-1].x + 1


def calculate_gear_ratio(gear: list[list[Point]], grid: list[list[str]]) -> int:
    ratio = 1
    for ngroup in gear:
        ratio *= get_int_value(ngroup, grid)

    return ratio

def get_int_value(ngroup: list[Point], grid: list[list[str]]) -> int:
    return int("".join(grid[point.y][point.x] for point in ngroup))



class Test:
    import pytest

    @pytest.mark.parametrize(
            ("case", "expected"),
            [
                ("""\
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
""", 467835),
                ],
            )
    def test_examples(self, case, expected):
        assert solution(case) == expected
