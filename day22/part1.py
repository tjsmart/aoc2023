from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from typing import NamedTuple
from typing import Self

from lib import collect_lines


class Vec2(NamedTuple):
    x: int
    y: int


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def xy(self) -> Vec2:
        return Vec2(self.x, self.y)

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(*map(int, s.split(',')))


@dataclass
class Brick:
    head: Vec3
    tail: Vec3

    def iter_xy(self) -> Iterator[Vec2]:
        assert self.head.x <= self.tail.x
        assert self.head.y <= self.tail.y
        for x in range(self.head.x, self.tail.x + 1):
            for y in range(self.head.y, self.tail.y + 1):
                yield Vec2(x, y)

    def height(self) -> int:
        assert self.head.z <= self.tail.z
        return self.tail.z - self.head.z + 1

    @classmethod
    def from_str(cls, s: str) -> Self:
        h_s, t_s = s.split('~')
        return cls(Vec3.from_str(h_s), Vec3.from_str(t_s))

def solution(s: str) -> int:
    bricks = collect_lines(s, Brick.from_str)
    bricks.sort(key=lambda b: b.head.z)

    important: set[int] = set()
    topography: dict[Vec2, tuple[int, int | None]] = defaultdict(lambda: (0, None))
    for bid, b in enumerate(bricks):
        z_to_bids: dict[int, set[int]] = defaultdict(set)
        for xy in b.iter_xy():
            z, obid = topography[xy]
            if obid is not None:
                z_to_bids[z].add(obid)

        max_z = max(z_to_bids or [0])
        max_z_bids = z_to_bids[max_z]
        if len(max_z_bids) == 1:
            important |= max_z_bids

        for xy in b.iter_xy():
            topography[xy] = (max_z + b.height(), bid)

    return len(bricks) - len(important)


class Test:
    import pytest

    EXAMPLE_INPUT = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
    EXPECTED_RESULT = 5

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
            ("0,0,0~0,0,0\n0,0,2~0,0,2", 1),
            ("0,0,0~3,0,0\n0,0,2~0,0,2", 1),
            ("0,0,0~0,3,0\n0,0,2~0,0,2", 1),
            ("0,0,0~0,0,3\n0,0,7~0,0,7", 1),
            ("0,0,0~0,0,0\n1,0,2~2,0,2", 2),
            ("0,0,0~0,0,0\n0,1,2~0,2,2", 2),
            ("0,0,0~0,0,0\n-2,0,2~-1,0,2", 2),
            ("0,0,0~0,0,0\n0,-2,2~0,-1,2", 2),
            ("0,0,0~0,0,0\n0,1,2~0,1,4", 2),
            ("""\
0,0,1~0,1,1
1,1,1~1,1,1
0,0,2~0,0,2
0,1,2~1,1,2
""", 3),
            ("""\
0,0,1~1,0,1
0,1,1~0,1,2
0,0,4~0,1,4
0,0,5~0,0,5
""", 2),

# D
# C
# B
# XA

# D
# CC
#  B
# AB
            ("""\
0,0,1~0,0,2
1,0,1~2,0,1
1,0,2~1,0,2
0,0,3~1,0,3
""", 3),
            ("""\
1,1,1~5,1,1
1,1,2~1,5,2
""", 1),
            ("""\
0,0,2~0,0,4
1,0,3~2,0,3
1,0,4~1,0,5
0,0,6~1,0,6
""", 3),
            ("""\
0,0,1~0,0,4
0,0,7~0,0,8
0,0,10~0,0,10
""", 1),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected


"""
0,0,1~0,1,1 <-- A
1,1,1~1,1,1 <-- B
0,0,2~0,0,2 <-- C
0,1,2~1,1,2 <-- D

It should return 3 because A is needed to support C
"""

"""
0,0,1~1,0,1 <- A
0,1,1~0,1,2 <- B
0,0,5~0,0,5 <- C
0,0,4~0,1,4 <- D

Answer should be 2 with A and C.
"""
