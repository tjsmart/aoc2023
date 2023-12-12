import itertools
from collections import deque
from typing import Literal

from .part1 import get_moves
from .part1 import get_starting_pos
from lib import collect_lines
from lib import Point


rotate_dir_to_rotate_map = {
    1: {
        Point(0, -1): Point(1, 0),
        Point(1, 0): Point(0, 1),
        Point(0, 1): Point(-1, 0),
        Point(-1, 0): Point(0, -1),
    },
    -1: {
        Point(0, -1): Point(-1, 0),
        Point(-1, 0): Point(0, 1),
        Point(0, 1): Point(1, 0),
        Point(1, 0): Point(0, -1),
    },
}


def solution(s: str) -> int:
    grid = collect_lines(s, list)
    loop, rd = get_loop(grid)

    rm = rotate_dir_to_rotate_map[rd]
    return len(get_inside_points(rm, grid, loop))


def get_loop(grid: list[list[str]]) -> tuple[list[Point], Literal[1, -1]]:
    start = get_starting_pos(grid)
    first_step, *_ = get_moves(start, grid)

    steps = [first_step]
    moves = [move for move in get_moves(first_step, grid) if move != start]
    (step,) = moves

    rd = 0
    direction = deque([step - first_step], maxlen=2)
    while step != start:
        steps.append(step)
        moves = [move for move in get_moves(step, grid) if move != steps[-2]]
        (step,) = moves
        direction.append(step - steps[-1])
        rd += rotation_dir(*direction)

    steps.append(step)
    return steps, sign(rd)


def rotation_dir(a: Point, b: Point) -> int:
    return 0 if a == b else 1 if R(a) == b else -1


def R(a: Point) -> Point:
    """90° ccw rotation"""
    return Point(-a.y, a.x)


def sign(x: int) -> Literal[1, -1]:
    assert x
    return 1 if x > 0 else -1


def get_inside_points(
    rm: dict[Point, Point], grid: list[list[str]], loop: list[Point]
) -> list[Point]:
    points_to_check = {
        Point(x, y) for x in range(len(grid[0])) for y in range(len(grid))
    } - set(loop)
    gps = []
    # replay every move along the loop
    for start, end in itertools.pairwise(itertools.chain(loop, [loop[0]])):
        move = end - start
        dn = rm[move]
        for lp in (start, end):
            n = lp + dn
            if n not in points_to_check:
                continue

            queue: set[Point] = {n}
            while queue:
                p = queue.pop()
                points_to_check.remove(p)
                gps.append(p)

                for n in p.iter_neighbors(diagonals=False):
                    if n in points_to_check and n not in queue:
                        queue.add(n)

    return gps


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
""",
                4,
            ),
            (
                """\
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
""",
                4,
            ),
            (
                """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""",
                8
                # ```
                #               1111111111
                #     01234567890123456789
                #
                #  0  OF----7F7F7F7F-7OOOO
                #  1  O|F--7||||||||FJOOOO
                #  2  O||OFJ||||||||L7OOOO
                #  3  FJL7L7LJLJ||LJIL-7OO
                #  4  L--JOL7IIILJS7F-7L7O
                #  5  OOOOF-JIIF7FJ|L7L7L7
                #  6  OOOOL7IF7||L7|IL7L7|
                #  7  OOOOO|FJLJ|FJ|F7|OLJ
                #  8  OOOOFJL-7O||O||||OOO
                #  9  OOOOL---JOLJOLJLJOOO
                # ```
            ),
            (
                """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""",
                10,
            ),
            (
                """\
S------7
|F----7|
||OOOO||
||OOOO||
|L-7F-J|
|II||II|
L--JL--J
""",
                4,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
