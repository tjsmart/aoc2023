from dataclasses import dataclass
from typing import Self

from lib import collect_lines
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
    symbols: list[Point] = []


    for j in range(len(grid)):
        for i in range(len(grid[0])):
            point = Point(i, j)
            c = grid[j][i]
            if c == '.':
                continue

            if c.isnumeric():
                if ngroups and immediately_follows(ngroups[-1], point):
                    ngroups[-1].append(point)
                else:
                    ngroups.append([point])
            else:
                # assume it is a symbol
                symbols.append(point)

    # print(ngroups, symbols)

    all_hits = []
    for symbol in symbols:
        hits = []
        for i, ngroup in enumerate(ngroups):
            if any(point.is_adjacent_to(symbol) for point in ngroup):
                hits.append(i)

        all_hits.extend(ngroups[i] for i in hits)
        for i in hits:
            try:
                ngroups.remove(i)
            except ValueError:
                pass

    return sum(map(lambda ngroup: get_int_from_ngroup(ngroup, grid), all_hits))


def immediately_follows(ngroup: list[Point], point: Point) -> bool:
    # assume we only need to check if point is immediately to the right of previous point
    return point.x == ngroup[-1].x + 1


def get_int_from_ngroup(ngroup: list[Point], grid: list[list[str]]) -> int:
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
""", 4361),
                ],
            )
    def test_examples(self, case, expected):
        assert solution(case) == expected
