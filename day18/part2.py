from lib import collect_lines
from lib import Point


def solution(s: str) -> int:
    moves = collect_lines(s, parse_move)
    return calc(moves)


def calc(moves: list[Point]) -> int:
    total = 1
    loc = Point(0, 0)

    for move in moves:
        loc += move
        match move:
            case Point(x, 0) if x > 0:
                total += x
            case Point(0, y) if y < 0:
                total += -(loc.x + 1) * y
            case Point(0, y) if y > 0:
                total += -(loc.x) * y

    return total


def parse_move(s: str) -> Point:
    code = s.split("#")[1].split(")")[0]
    count = int(code[:5], 16)
    match code[-1]:
        case "0":  # "R"
            return Point(count, 0)
        case "1":  # "D"
            return Point(0, -count)
        case "2":  # "L"
            return Point(-count, 0)
        case "3":  # "U"
            return Point(0, count)
        case _:
            raise ValueError(f"bad dir code: {code[-1]}")


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
    EXPECTED_RESULT = 952408144115

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
