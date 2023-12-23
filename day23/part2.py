from collections import defaultdict
from collections import deque
from dataclasses import dataclass
from typing import Self

from lib import FrozenGrid
from lib import NegInf
from lib import NegInfType
from lib import Point


@dataclass
class OpenPath:
    start: Point
    sdir: Point
    end: Point
    edir: Point
    length: int

    def flipped(self) -> Self:
        return OpenPath(self.end, self.edir, self.start, self.sdir, self.length)

@dataclass
class DeadEndPath:
    start: Point
    sdir: Point
    end: Point
    edir: Point
    length: int



@dataclass
class ClosedPath:
    start: Point
    sdir: Point


type Path = OpenPath | ClosedPath | DeadEndPath


def solution(s: str) -> int:
    grid = FrozenGrid.from_str(s)
    start = Point(1, 0)
    end = Point(grid.col_len() - 2, grid.row_len() - 1)

    junctions: dict[Point, dict[Point, Path | None]] = defaultdict(default_junction)
    queue: list[tuple[Point, set[Point], int]] = [(start, {start}, 0)]
    best = NegInf
    while queue:
        loc, been, length = queue.pop()

        for d, p in junctions[loc].items():
            if p is None:
                p = explore(loc, d, grid)
                junctions[loc][d] = p
                if isinstance(p, OpenPath):
                    junctions[p.end][p.edir] = p.flipped()

            match p:
                case ClosedPath():
                    continue

                case DeadEndPath():
                    if p.end == end:
                        best = max(best, length + p.length)
                        continue

                case OpenPath():
                    if p.end in been:
                        continue

                    queue.append((p.end, been | {p.end}, length + p.length))

                case _:
                    assert False, "uh oh!"

    assert not isinstance(best, NegInfType)
    return best


def explore(start: Point, sdir: Point, grid: FrozenGrid) -> Path:
    last = start
    loc = start + sdir

    if not grid.in_bounds(loc) or grid[loc] == '#':
        return ClosedPath(start, sdir)

    length = 1
    while True:
        possible_steps: list[Point] = [
            n for n in loc.iter_neighbors(diagonals=False)
            if n != last and grid.in_bounds(n) and grid[n] != '#'
        ]

        match possible_steps:
            case []:
                return DeadEndPath(start, sdir, loc, last - loc, length)
            case [n]:
                length += 1
                last, loc = loc, n
            case _:
                return OpenPath(start, sdir, loc, last - loc, length)


def default_junction() -> dict[Point, Path | None]:
    return {
        Point(1, 0): None,
        Point(0, -1): None,
        Point(-1, 0): None,
        Point(0, 1): None,
    }

class Test:
    import pytest

    EXAMPLE_INPUT = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
    EXPECTED_RESULT = 154

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
