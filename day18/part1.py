from .part2 import calc
from lib import collect_lines
from lib import Point


def solution(s: str) -> int:
    moves = collect_lines(s, parse_move)
    return calc(moves)


def parse_move(s: str) -> Point:
    dir_s, count, _ = s.split()
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

    return dir * int(count)


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
