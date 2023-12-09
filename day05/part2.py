from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from itertools import batched
from typing import Self

from lib import collect_block_statements


@dataclass
class Almanac:
    seeds: list[Range]
    maps: list[Map]

    @classmethod
    def from_str(cls, s: str) -> Self:
        seed_str, s = s.split("\n\n", 1)
        pairs = batched(map(int, seed_str.split(":")[1].strip().split()), 2)
        seeds = list(map(lambda pair: Range(*pair), pairs))
        maps = collect_block_statements(s, parse_map_block)
        return cls(seeds, maps)


@dataclass
class Map:
    name: str
    entries: list[MapEntry] = field(default_factory=list)

    def sort_on_src(self, reverse: bool = False) -> list[MapEntry]:
        return sorted(
            self.entries, key=lambda entry: (entry.src, entry.dst), reverse=reverse
        )

    def sort_on_dst(self, reverse: bool = False) -> list[MapEntry]:
        return sorted(
            self.entries, key=lambda entry: (entry.dst, entry.src), reverse=reverse
        )


@dataclass(order=True)
class MapEntry:
    src: Range
    dst: Range

    def get(self, key: int) -> int:
        if self.src.start <= key <= self.src.end:
            return self.dst.start + key - self.src.start
        return key


@dataclass(order=True)
class Range:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def __contains__(self, key: int) -> int:
        return self.start <= key < self.start + self.length


def overlap(a: Range, b: Range) -> tuple[int, int]:
    """
    a.start                  a.end
    |                        |

            |  -- overlap -- |
            |                      |
            b.start                b.end
    """
    start = max(a.start, b.start)
    end = min(a.end, b.end)
    # if end < start, there is no overlap
    return start, end


def map_items(items: list[Range], map_: Map) -> list[Range]:
    items = sorted(items, reverse=True)
    entries = map_.sort_on_src(reverse=True)

    assert items and entries
    entry = entries.pop()
    mapped: list[Range] = []
    while items:
        item = items.pop()

        if item.end < entry.src.start:
            mapped.append(item)
            continue

        if item.start > entry.src.end:
            items.append(item)
            try:
                entry = entries.pop()
            except IndexError:
                break
            else:
                continue

        # there is overlap
        ds = entry.src.start - item.start
        de = item.end - entry.src.end
        if ds > 0:
            # non-overlapping portion at start is not mappable
            mapped.append(Range(item.start, ds))
            ds = 0

        if de > 0:
            # non-overlapping portion at end may be mappable by next entry
            items.append(Range(item.end - de + 1, de))
            de = 0

        start, end = overlap(item, entry.src)
        length = end - start + 1
        mapped_start = entry.get(start)
        mapped.append(Range(mapped_start, length))

    # add any remaining items that could not be mapped
    mapped.extend(items)

    return mapped


def solution(s: str) -> int:
    almanac = Almanac.from_str(s)
    items = almanac.seeds
    for map_ in almanac.maps:
        items = map_items(items, map_)

    return min(items).start


def parse_map_block(s: str) -> Map:
    lines = s.splitlines()
    name, lines = lines[0].split()[0], lines[1:]
    map_ = Map(name)
    for line in lines:
        dst_start, src_start, length = map(int, line.split())
        map_.entries.append(
            MapEntry(
                dst=Range(dst_start, length),
                src=Range(src_start, length),
            )
        )

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
