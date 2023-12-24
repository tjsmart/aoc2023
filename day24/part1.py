from dataclasses import dataclass
from functools import cached_property
from itertools import combinations
from typing import NamedTuple
from typing import Self

from lib import collect_lines


class Vec2(NamedTuple):
    x: float
    y: float


@dataclass(frozen=True)
class HailStone:
    p: Vec2
    v: Vec2

    @cached_property
    def m(self) -> float:
        return self.v.y / self.v.x

    @classmethod
    def from_str(cls, s: str) -> Self:
        p_s, v_s = s.split(" @ ")
        px, py, _ = (int(x) for x in p_s.split(", "))
        vx, vy, _ = (int(x) for x in v_s.split(", "))
        return cls(Vec2(px, py), Vec2(vx, vy))


def solution(
    s: str, lbound: int = 200000000000000, rbound: int = 400000000000000
) -> int:
    stones = collect_lines(s, HailStone.from_str)
    total = 0
    for a, b in combinations(stones, 2):
        if (
            (cross := get_cross(a, b))
            and (lbound <= cross.x <= rbound)
            and (lbound <= cross.y <= rbound)
        ):
            total += 1

    return total


def get_cross(a: HailStone, b: HailStone) -> Vec2 | None:
    if a.m == b.m:
        return None

    x = get_x(a, b)
    y = get_y(a, x)
    cross = Vec2(x, y)

    if (a.p.x < cross.x and a.v.x < 0) or (a.p.x > cross.x and a.v.x > 0):
        return None

    if b.p.x < cross.x and b.v.x < 0 or (b.p.x > cross.x and b.v.x > 0):
        return None

    return cross


def get_x(a: HailStone, b: HailStone) -> float:
    return (b.p.y - a.p.y + a.m * a.p.x - b.m * b.p.x) / (a.m - b.m)


def get_y(a: HailStone, x: float) -> float:
    return a.m * (x - a.p.x) + a.p.y


class Test:
    import pytest

    EXAMPLE_INPUT = """\
19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @ 1, -5, -3
"""
    EXPECTED_RESULT = 2

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case, lbound=7, rbound=27) == expected
