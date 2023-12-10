from lib import collect_lines
from lib import Point


def solution(s: str) -> int:
    grid = collect_lines(s, list)
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
            if pos == start:
                return (len(steps) + 1) // 2

            steps.append(pos)
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

    EXAMPLE_INPUT = """\
.....
.F-7.
.|.|.
.L-J.
.....
"""
    EXPECTED_RESULT = 0

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
(
"""\
.....
.S-7.
.|.|.
.L-J.
.....
""", 4
), (
"""\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""", 4
), (
"""\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""", 8
), (
"""\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""", 8
),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
