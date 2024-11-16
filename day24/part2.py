from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import NamedTuple

import numpy.linalg

from lib import collect_lines


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, o: tuple[int, int, int]) -> Vec3:
        return Vec3(self.x + o[0], self.y + o[1], self.z + o[2])

    def __radd__(self, o: tuple[int, int, int]) -> Vec3:
        return Vec3(self.x + o[0], self.y + o[1], self.z + o[2])

    def __sub__(self, o: tuple[int, int, int]) -> Vec3:
        return Vec3(self.x - o[0], self.y - o[1], self.z - o[2])

    def __rsub__(self, o: tuple[int, int, int]) -> Vec3:
        return Vec3(self.x - o[0], self.y - o[1], self.z - o[2])

    def __mul__(self, v: int) -> Vec3:
        return Vec3(self.x * v, self.y * v, self.z * v)

    def __rmul__(self, v: int) -> Vec3:
        return Vec3(self.x * v, self.y * v, self.z * v)

    def __floordiv__(self, v: int) -> Vec3:
        return Vec3(self.x // v, self.y // v, self.z // v)

    def __rfloordiv__(self, v: int) -> Vec3:
        return Vec3(self.x // v, self.y // v, self.z // v)


@dataclass(frozen=True)
class Projectile:
    p0: Vec3
    v: Vec3


def solution(s: str) -> int:
    stones = collect_lines(s, parse)

    avg = Vec3(
        round(statistics.mean(st.p0.x for st in stones)),
        round(statistics.mean(st.p0.y for st in stones)),
        round(statistics.mean(st.p0.z for st in stones)),
    )

    stones = [Projectile(st.p0 - avg, st.v) for st in stones]

    x, _, y, _ = map(round, do_the_dirty(stones[:5]))
    _, _, z, _ = map(round, do_the_dirtz(stones[:5]))
    return x + y + z + avg.x + avg.y + avg.z


def parse(s: str) -> Projectile:
    p_s, v_s = s.split(" @ ")
    px, py, pz = (int(x) for x in p_s.split(", "))
    vx, vy, vz = (int(x) for x in v_s.split(", "))
    return Projectile(Vec3(px, py, pz), Vec3(vx, vy, vz))


def do_the_dirty(stones: list[Projectile]) -> tuple[float, float, float, float]:
    assert len(stones) == 5
    st0, *rest = stones
    mat = numpy.array(
        [
            [
                st0.v.y - stn.v.y,
                stn.p0.y - st0.p0.y,
                stn.v.x - st0.v.x,
                st0.p0.x - stn.p0.x,
            ]
            for stn in rest
        ]
    )

    delta = numpy.array(
        [
            st0.p0.x * st0.v.y
            - st0.p0.y * st0.v.x
            + stn.p0.y * stn.v.x
            - stn.p0.x * stn.v.y
            for stn in rest
        ]
    )

    ans = numpy.linalg.inv(mat).dot(delta)
    return ans


def do_the_dirtz(stones: list[Projectile]) -> tuple[float, float, float, float]:
    assert len(stones) == 5
    st0, *rest = stones
    mat = numpy.array(
        [
            [
                st0.v.z - stn.v.z,
                stn.p0.z - st0.p0.z,
                stn.v.x - st0.v.x,
                st0.p0.x - stn.p0.x,
            ]
            for stn in rest
        ]
    )

    delta = numpy.array(
        [
            st0.p0.x * st0.v.z
            - st0.p0.z * st0.v.x
            + stn.p0.z * stn.v.x
            - stn.p0.x * stn.v.z
            for stn in rest
        ]
    )

    ans = numpy.linalg.inv(mat).dot(delta)
    return ans


class Test:
    import pytest

    EXAMPLE_INPUT = """\
19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @ 1, -5, -3
"""
    EXPECTED_RESULT = 47

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
