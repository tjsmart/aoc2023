from collections import deque
from dataclasses import dataclass
from typing import Literal
from typing import Self

from lib import collect_lines
from lib import Point


rotate_dir_to_rotate_map = {
    1: {
        Point(1, 0): Point(0, 1),
        Point(-1, 0): Point(0, -1),
        Point(0, 1): Point(-1, 0),
        Point(0, -1): Point(1, 0),
    },
    -1: {
        Point(1, 0): Point(0, -1),
        Point(-1, 0): Point(0, 1),
        Point(0, 1): Point(1, 0),
        Point(0, -1): Point(-1, 0),
    },
}




@dataclass
class Instruction:
    dir: Point
    count: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        dir_s, count, _, = s.split()
        match dir_s:
            case "R":
                dir = Point(1, 0)
            case "L":
                dir = Point(-1, 0)
            case "U":
                dir = Point(0, 1)
            case "D":
                dir = Point(0, -1)
            case _:
                assert False, f"bad dir_s: {dir_s}"

        return cls(dir, int(count))


def solution(s: str) -> int:
    instructions = collect_lines(s, Instruction.from_str)
    loc = Point(0, 0)
    dugout: set[Point] = {loc}
    moves: deque[Point] = deque(maxlen=2)
    rotation = 0
    for instruction in instructions:
        for _ in range(instruction.count):
            loc += instruction.dir
            dugout.add(loc)

        moves.append(instruction.dir)
        if len(moves) == 2:
            rotation += rotation_dir(*moves)


    inside_point = find_an_inside_point(instructions, dugout, rotation)
    inside = get_inside_points(inside_point, dugout)

    return len(inside) + len(dugout)

def find_an_inside_point(instructions: list[Instruction], dugout: set[Point], rotation: int) -> Point:
    rmap= rotate_dir_to_rotate_map[sign(rotation)]
    loc = Point(0, 0)
    for instruction in instructions:
        for _ in range(instruction.count):
            loc += instruction.dir
            candidate = loc + rmap[instruction.dir]
            if candidate not in dugout:
                return candidate
    assert False, "uh oh! 😲"

def get_inside_points(inside_point: Point, dugout: set[Point]) -> set[Point]:
    queue: list[Point] = [inside_point]
    inside_points: set[Point] = {inside_point}
    while queue:
        loc = queue.pop()
        for n in loc.iter_neighbors():
            if n not in dugout and n not in inside_points:
                queue.append(n)
                inside_points.add(n)

    return inside_points



def rotation_dir(a: Point, b: Point) -> int:
    return 0 if a == b else 1 if R(a) == b else -1


def R(a: Point) -> Point:
    """90° ccw rotation"""
    return Point(-a.y, a.x)


def sign(x: int) -> Literal[1, -1]:
    assert x
    return 1 if x > 0 else -1

class Test:
    import pytest

    EXAMPLE_INPUT = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
    EXPECTED_RESULT = 62

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
