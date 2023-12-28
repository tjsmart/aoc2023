"""
Shortest path to any parallel universe is taking the edge path which in the example as well
as the input is completely open.

Breaking the multiverse into quadrants:


                    |
                    |
            2       |       1
                    |
                    |
    -----------------------------------
                    |
                    |
            3       |       4
                    |
                    |

We will always arrive to a new universe in the
- 1st quadrant from the lower left
- 2nd quadrant from the lower right
- 3rd quadrant from the upper right
- 4th quadrant from the upper left
"""
from __future__ import annotations

import math
import operator
from collections.abc import Iterator
from collections.abc import Sequence
from dataclasses import dataclass
from typing import SupportsIndex

from lib import FrozenGrid
from lib import Point


type GridWalk = list[set[Point]]


def solution(s: str, steps: int = 26501365) -> int:
    grid = FrozenGrid.from_str(s)
    assert grid.row_len() == grid.col_len()

    sp = grid.find("S")
    max_xy = grid.row_len() - 1

    total = 0
    total += calc_center(sp, grid, steps)
    for side in (
        Point(0, sp.y),  # from left
        Point(sp.x, 0),  # from top
        Point(max_xy, sp.y),  # from right
        Point(sp.x, max_xy),  # from bottom
    ):
        total += calc_side(sp, grid, steps, side)

    for angle in (
        Point(0, max_xy),  # from bottom left
        Point(max_xy, max_xy),  # from bottom right
        Point(max_xy, 0),  # from top right
        Point(0, 0),  # from top left
    ):
        total += calc_angle(sp, grid, steps, angle)

    return total


def calc_center(sp: Point, grid: FrozenGrid, steps: int) -> int:
    gw = walk_grid(sp, grid)
    return get_gw_total(gw, steps)


def calc_side(sp: Point, grid: FrozenGrid, steps: int, side: Point) -> int:
    if steps <= sp.x:
        return 0

    gw = walk_grid(side, grid)
    max_i = math.ceil((steps - sp.x - 1) / grid.row_len())

    total = 0
    for i in range(max_i, 0, -1):
        steps_to_grid = sp.x + 1 + grid.row_len() * (i - 1)
        steps_on_grid = steps - steps_to_grid
        if steps_on_grid >= len(gw):
            break
        total += get_gw_total(gw, steps_on_grid)
    else:
        return total

    q, r = divmod(i, 2)
    total += (q + r) * get_gw_odd_max(gw)
    total += q * get_gw_even_max(gw)

    return total


def calc_angle(sp: Point, grid: FrozenGrid, steps: int, angle: Point) -> int:
    steps_to_escape_center = sp.x + sp.y + 2
    if steps < steps_to_escape_center:
        return 0

    gw = walk_grid(angle, grid)
    steps_to_cross_grid = grid.row_len()
    max_i = math.ceil((steps - steps_to_escape_center) / steps_to_cross_grid)

    total = 0
    for i in range(max_i, 0, -1):
        steps_to_grid = steps_to_escape_center + steps_to_cross_grid * (i - 1)
        steps_on_grid = steps - steps_to_grid
        if steps_on_grid >= len(gw):
            break
        total += get_gw_total(gw, steps_on_grid) * i

    else:
        return total

    q, r = divmod(i, 2)
    total += sum_of_n_odd_numbers(q + r) * get_gw_odd_max(gw)
    total += sum_of_n_even_numbers(q) * get_gw_even_max(gw)

    return total


def sum_of_n_odd_numbers(n: int) -> int:
    return n**2


def sum_of_n_even_numbers(n: int) -> int:
    return n * (n + 1)


def get_gw_total(gw: GridWalk, steps_on_grid: int) -> int:
    odd = steps_on_grid % 2
    return sum(len(x) for i, x in enumerate(gw) if i % 2 == odd and i <= steps_on_grid)


def get_gw_odd_max(gw: GridWalk) -> int:
    return sum(len(x) for x in gw[1::2])


def get_gw_even_max(gw: GridWalk) -> int:
    return sum(len(x) for x in gw[::2])


def walk_grid(sp: Point, grid: FrozenGrid) -> GridWalk:
    visited: set[Point] = set()
    gw: GridWalk = []
    edge: set[Point] = {sp}
    while edge:
        visited |= edge
        gw.append(edge)
        edge = {sp for ep in edge for sp in get_steps(ep, grid, visited)}

    return gw


def get_steps(l: Point, grid: FrozenGrid, visited: set[Point]) -> Iterator[Point]:
    for n in l.iter_neighbors(diagonals=False):
        if n in visited or not grid.in_bounds(n):
            continue

        if grid[n.y][n.x] != "#":
            yield n


def brute_force(s: str, steps: int) -> int:
    grid = FrozenGrid.from_str(s)
    sp = grid.find("S")
    mvgrid = Multiverse(grid)

    even_locations: set[Point] = {sp}
    odd_locations: set[Point] = set()
    edge: set[Point] = {sp}
    for i in range(1, steps + 1):
        edge = {sp for ep in edge for sp in get_brute_steps(ep, mvgrid, even_locations, odd_locations)}

        if i % 2:
            odd_locations |= edge
        else:
            even_locations |= edge

    return len(odd_locations) if steps % 2 else len(even_locations)


def get_brute_steps(l: Point, grid: Multiverse, even_locations: set[Point], odd_locations: set[Point]) -> Iterator[Point]:
    for n in l.iter_neighbors(diagonals=False):
        if n in even_locations or n in odd_locations:
            continue

        if grid[n.y][n.x] != "#":
            yield n


@dataclass
class RepeatingSequence[T]:
    _x: Sequence[T]

    def __getitem__(self, __key: SupportsIndex) -> T:
        mapped_key = operator.index(__key) % len(self._x)
        return self._x[mapped_key]


@dataclass
class Multiverse[T]:
    _x: Sequence[Sequence[T]]

    def __getitem__(self, __key: SupportsIndex) -> RepeatingSequence[T]:
        mapped_key = operator.index(__key) % len(self._x)
        return RepeatingSequence(self._x[mapped_key])


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

    @pytest.mark.parametrize(
        ("steps", "expected"),
        [
            (6, 16),
            (10, 50),
            (50, 1594),
            (100, 6536),
            (500, 167004),
            (1000, 668697),
            (5000, 16733044),
        ],
    )
    def test_examples(self, steps, expected):
        assert brute_force(self.EXAMPLE_INPUT, steps=steps) == expected
        # assert solution(self.EXAMPLE_INPUT, steps=steps) == expected


    @pytest.mark.parametrize(
            "steps", [6, 10, 50, 100, 500]
    )
    def test_against_brute_force_solution(self, steps):
        # NOTE: brute_force has some bug with 500
        from pathlib import Path
        real_input = (Path(__file__).resolve().parent / "input.txt").read_text()
        expected_result = brute_force(real_input, steps=steps)
        actual_result = solution(real_input, steps=steps)
        assert actual_result == expected_result
