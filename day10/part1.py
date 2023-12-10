from lib import collect_lines
from lib import Point


def solution(s: str) -> int:
    grid = collect_lines(s, list)
    loop = get_loop(grid)
    return len(loop) // 2


def get_loop(grid: list[list[str]]) -> list[Point]:
    start = get_starting_pos(grid)
    first_step, *_ = get_moves(start, grid)

    steps = [first_step]
    moves = [move for move in get_moves(first_step, grid) if move != start]
    (step,) = moves

    while step != start:
        steps.append(step)
        moves = [move for move in get_moves(step, grid) if move != steps[-2]]
        (step,) = moves

    steps.append(step)
    return steps


def get_starting_pos(grid: list[list[str]]) -> Point:
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                return Point(x, y)
    assert False, "Could not find S"


def get_moves(p: Point, grid: list[list[str]]) -> list[Point]:
    c = grid[p.y][p.x]
    match c:
        case "|":
            moves = []
            if x := can_move_up(p, grid):
                moves.append(x)
            if x := can_move_down(p, grid):
                moves.append(x)
            return moves

        case "-":
            moves = []
            if x := can_move_left(p, grid):
                moves.append(x)
            if x := can_move_right(p, grid):
                moves.append(x)
            return moves

        case "F":
            moves = []
            if x := can_move_right(p, grid):
                moves.append(x)
            if x := can_move_down(p, grid):
                moves.append(x)
            return moves

        case "J":
            moves = []
            if x := can_move_left(p, grid):
                moves.append(x)
            if x := can_move_up(p, grid):
                moves.append(x)
            return moves

        case "7":
            moves = []
            if x := can_move_left(p, grid):
                moves.append(x)
            if x := can_move_down(p, grid):
                moves.append(x)
            return moves

        case "L":
            moves = []
            if x := can_move_right(p, grid):
                moves.append(x)
            if x := can_move_up(p, grid):
                moves.append(x)
            return moves

        case "S":
            moves = []
            if x := can_move_up(p, grid):
                moves.append(x)
            if x := can_move_right(p, grid):
                moves.append(x)
            if x := can_move_down(p, grid):
                moves.append(x)
            if x := can_move_left(p, grid):
                moves.append(x)
            return moves

        case _:
            return []


def can_move_up(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (0, -1)
    if grid[n.y][n.x] in ("F", "7", "|", "S"):
        return n


def can_move_down(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (0, 1)
    if grid[n.y][n.x] in ("J", "L", "|", "S"):
        return n


def can_move_right(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (1, 0)
    if grid[n.y][n.x] in ("J", "7", "-", "S"):
        return n


def can_move_left(p: Point, grid: list[list[str]]) -> Point | None:
    n = p + (-1, 0)
    if grid[n.y][n.x] in ("L", "F", "-", "S"):
        return n


class Test:
    import pytest

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
""",
                4,
            ),
            (
                """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""",
                4,
            ),
            (
                """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""",
                8,
            ),
            (
                """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""",
                8,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
