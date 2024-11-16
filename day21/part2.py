"""
More robust solution is possible, but who has the time?
Thought:
    perform complete grid walk in a 3x3 universe, saving off the points visited on each step per square:
        {
            (0,0): [{(5, 5)}, {(4, 5), (5, 4)} ...]   # points in middle square
            (1,0): [{}, {}, ..., {(0, 5)}, {(0, 6), (1, 5)} ...]   # points in right square
            ... # so on for the other 7 squares
        }
    use this to project larger steps
"""
import math
from collections.abc import Iterator

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
