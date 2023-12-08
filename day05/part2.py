from dataclasses import dataclass
from dataclasses import field
from itertools import batched
from itertools import chain
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

    def inv_get(self, value: int) -> int:
        if self.dst_r <= value <= self.dst_r + self.r_len:
            return self.src_r + value - self.dst_r
        return value


@dataclass
class Map:
    name: str
    ranges: list[Range] = field(default_factory=list)

    def get(self, key: int) -> int:
        for r in self.ranges:
            if (value := r.get(key)) != key:
                return value
        return key

    def inv_get(self, value: int) -> int:
        for r in self.ranges:
            if (key := r.inv_get(value)) != value:
                return key
        return value

    def add(self, dst_r: int, src_r: int, r_len: int) -> None:
        self.ranges.append(Range(dst_r, src_r, r_len))


@dataclass
class SeedRange:
    start: int
    length: int

    def __contains__(self, key: int) -> int:
        return self.start <= key < self.start + self.length


@dataclass
class Almanac:
    seed_ranges: list[SeedRange]
    maps: list[Map]

    @classmethod
    def from_str(cls, s: str) -> Self:
        seed_str, s = s.split("\n\n", 1)
        pairs = batched(map(int, seed_str.split(":")[1].strip().split()), 2)
        seed_ranges = list(map(lambda pair: SeedRange(*pair), pairs))
        maps = collect_block_statements(s, parse_map_block)
        return cls(seed_ranges, maps)

    def get_min_location_number(self) -> int:
        for location_number in range(1, 1_000_000_000):
            if self.is_valid_location_number(location_number):
                return location_number

        assert False, "Failed to find the lowest location number!"

    def is_valid_location_number(self, location_number: int) -> bool:
        value = location_number
        for map in reversed(self.maps):
            value = map.inv_get(value)

        return any(value in seed_range for seed_range in self.seed_ranges)

    def get_location_number(self, seed: int) -> int:
        value = seed
        for map in self.maps:
            value = map.get(value)

        return value


def solution(s: str) -> int:
    almanac = Almanac.from_str(s)
    return almanac.get_min_location_number()


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

    EXAMPLE_INPUT = """\
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
"""

    @pytest.mark.parametrize(
        ("case", "expected"),
        [(EXAMPLE_INPUT, 46)],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected

    @pytest.mark.parametrize("seed", chain(range(79, 79 + 14), range(55, 55 + 13)))
    def test_is_valid_seed_number(self, seed):
        almanac = Almanac.from_str(self.EXAMPLE_INPUT)

        location_number = almanac.get_location_number(seed)
        assert almanac.is_valid_location_number(location_number)
