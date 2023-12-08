from dataclasses import dataclass
from dataclasses import field
from typing import Self

from lib import collect_block_statements


@dataclass
class Range:
    dst_r: int
    src_r: int
    r_len: int

    def get(self, key: int) -> int:
        if self.src_r <= key <= self.src_r + self.r_len:
            return self.dst_r + key - self.src_r
        return key


@dataclass
class Map:
    name: str
    ranges: list[Range] = field(default_factory=list)

    def get(self, key: int) -> int:
        for r in self.ranges:
            if (value := r.get(key)) != key:
                return value
        return key

    def add(self, dst_r: int, src_r: int, r_len: int) -> None:
        self.ranges.append(Range(dst_r, src_r, r_len))


@dataclass
class Almanac:
    seeds: list[int]
    maps: list[Map]

    @classmethod
    def from_str(cls, s: str) -> Self:
        seed_str, s = s.split("\n\n", 1)
        seeds = list(map(int, seed_str.split(":")[1].strip().split()))
        maps = collect_block_statements(s, parse_map_block)
        return cls(seeds, maps)

    def get_location_numbers(self) -> list[int]:
        location_numbers = []
        for seed in self.seeds:
            value = seed
            for map in self.maps:
                value = map.get(value)

            location_numbers.append(value)
        return location_numbers


def solution(s: str) -> int:
    a = Almanac.from_str(s)
    return min(a.get_location_numbers())


def parse_map_block(s: str) -> Map:
    lines = s.splitlines()
    name, lines = lines[0].split()[0], lines[1:]
    map_ = Map(name)
    for line in lines:
        dst_r, src_r, r_len = map(int, line.split())
        map_.add(dst_r, src_r, r_len)

    return map_


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""",
                35,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
