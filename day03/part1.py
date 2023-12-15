import string
from dataclasses import dataclass
from dataclasses import field

from lib import collect_lines
from lib import Point


symbols = ["#", "%", "&", "*", "+", "-", "/", "=", "@", "$"]


@dataclass
class Number:
    s: list[str] = field(default_factory=list)
    g: bool = False


def solution(s: str) -> int:
    grid = collect_lines(s, list)

    sum = 0
    for y, row in enumerate(grid):
        number = Number()
        for x, c in enumerate(row):
            if c in string.digits:
                number.s.append(c)
                if not number.g:
                    number.g = find_gear(Point(x, y), grid)

            else:
                if number.g:
                    sum += int("".join(number.s))

                number = Number()

        if number.g:
            sum += int("".join(number.s))

    return sum


def find_gear(p: Point, grid: list[list[str]]) -> bool:
    return any(
        grid[n.y][n.x] in symbols
        for n in p.iter_neighbors()
        if 0 <= n.y < len(grid) and 0 <= n.x < len(grid[0])
    )


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""",
                4361,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
