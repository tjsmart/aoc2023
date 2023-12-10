import itertools
from dataclasses import dataclass

from lib import collect_lines
from lib import Point


@dataclass
class Group:
    ps: list[Point]
    i: bool


rotate_right = {Point(0, -1): Point(1, 0), Point(1, 0): Point(0, 1), Point(0, 1): Point(-1, 0), Point(-1, 0): Point(0, -1)}
rotate_left = {Point(0, -1): Point(-1, 0), Point(-1, 0): Point(0, 1), Point(0, 1): Point(1, 0), Point(1, 0): Point(0, -1)}

def solution(s: str) -> int:
    grid = collect_lines(s, list)
    loop = get_loop(grid)
    points_to_check = list({Point(x, y) for x in range(len(grid[0])) for y in range(len(grid))} - set(loop))

    groups = {"left": Group([], True), "right": Group([], True)}
    # iterate every step along the loop
    for start, end in itertools.pairwise(itertools.chain(loop, [loop[0]])):
        move = end - start

        for k, dn in (("left", rotate_left[move]), ("right", rotate_right[move])):
            for lp in (start, end):
                n = lp + dn
                if n not in points_to_check:
                    continue

                g = groups[k]
                queue: list[Point] = [n]
                while queue:
                    p = queue.pop()
                    points_to_check.remove(p)
                    g.ps.append(p)

                    for n in p.iter_neighbors(diagonals=False):
                        if out_of_bounds(n, grid):
                            g.i = False
                        elif n in points_to_check and n not in queue:
                            queue.append(n)

    for g in groups.values():
        if g.i:
            return len(g.ps)


    assert False, "uh oh!"



def out_of_bounds(p: Point, grid: list[list[str]]) -> bool:
    return p.x < 0 or p.x >= len(grid[0]) or p.y < 0 or p.y >= len(grid)


def get_loop(grid: list[list[str]]) -> list[Point]:
    start = get_starting_pos(grid)

    possible_first_steps = []
    for m, cs in (
        ((1, 0), ('J', '7', '-')),
        ((-1, 0), ('L', 'F', '-')),
        ((0, -1), ('F', '7', '|')),
        ((0, 1), ('L', 'J', '|')),
    ):
        p = start + m
        if grid[p.y][p.x] in cs:
            possible_first_steps.append(p)


    # for n in start.iter_neighbors(diagonals=False):
    for n in possible_first_steps:
        moves = get_moves(n, grid)
        queue: list[tuple[list[Point], Point]] = [([n], pos) for pos in moves if pos != start]
        while queue:
            steps, pos = queue.pop()
            steps.append(pos)
            if pos == start:
                return steps

            moves = get_moves(pos, grid)
            if not moves:
                # dead end
                continue

            queue.extend((steps, move) for move in moves if move not in steps)

    assert False, "uh oh!"





def get_starting_pos(grid: list[list[str]]) -> Point:
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                return Point(x, y)
    assert False, "Could not find S"



def get_moves(p: Point, grid: list[list[str]]) -> list[Point]:
    c = grid[p.y][p.x]
    match c:
        case '|':
            moves = []
            if (x := can_move_up(p, grid)):
                moves.append(x)
            if (x := can_move_down(p, grid)):
                moves.append(x)
            return moves

        case '-':
            moves = []
            if (x := can_move_left(p, grid)):
                moves.append(x)
            if (x := can_move_right(p, grid)):
                moves.append(x)
            return moves

        case 'F':
            moves = []
            if (x := can_move_right(p, grid)):
                moves.append(x)
            if (x := can_move_down(p, grid)):
                moves.append(x)
            return moves

        case 'J':
            moves = []
            if (x := can_move_left(p, grid)):
                moves.append(x)
            if (x := can_move_up(p, grid)):
                moves.append(x)
            return moves

        case '7':
            moves = []
            if (x := can_move_left(p, grid)):
                moves.append(x)
            if (x := can_move_down(p, grid)):
                moves.append(x)
            return moves

        case 'L':
            moves = []
            if (x := can_move_right(p, grid)):
                moves.append(x)
            if (x := can_move_up(p, grid)):
                moves.append(x)
            return moves

        case _:
            return []


def can_move_up(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (0, -1)
    if grid[n.y][n.x] in ('F', '7', '|', 'S'):
        return n

def can_move_down(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (0, 1)
    if grid[n.y][n.x] in ('J', 'L', '|', 'S'):
        return n

def can_move_right(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (1, 0)
    if grid[n.y][n.x] in ('J', '7', '-', 'S'):
        return n

def can_move_left(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (-1, 0)
    if grid[n.y][n.x] in ('L', 'F', '-', 'S'):
        return n

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
""", 4
), (
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
""", 4
), (
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
""", 8
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
), (
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
""", 10
),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
