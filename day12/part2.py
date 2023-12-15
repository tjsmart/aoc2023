from functools import lru_cache

from lib import collect_lines


def solution(s: str) -> int:
    readings = collect_lines(s, parse)
    return sum(map(lambda reading: calc_expand(*reading), readings))


def calc_expand(record: str, counts: tuple[int, ...]) -> int:
    return calc(*expand(record, counts))


def expand(record: str, counts: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join(record for _ in range(5)), tuple(list(counts) * 5)


@lru_cache
def calc(record: str, counts: tuple[int, ...]) -> int:
    if not counts:
        return "#" not in record

    count = counts[0]

    i = -1
    ars = 0
    while True:
        i += 1
        if i + count > len(record):
            return ars

        p = record[i - 1] if i else ""
        batch = record[i : i + count]
        n = record[i + count] if len(record) > i + count else ""

        if p == "#":
            return ars

        if "." in batch or n == "#":
            continue

        ars += calc(record[i + count + 1 :].lstrip('.'), counts[1:])


def parse(line: str) -> tuple[str, tuple[int, ...]]:
    x, y = line.split()
    return x, tuple(map(int, y.strip().split(",")))


class Test:
    import pytest

    EXAMPLE_INPUT = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    EXPECTED_RESULT = 525152

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected

    @pytest.mark.parametrize(
        ("record", "counts", "expected"),
        [
            ("#", (1,), 1),
            ("?", (1,), 1),
            ("??", (1,), 2),
            ("?#", (1,), 1),
            ("#?", (1,), 1),
            ("##", (2,), 1),
            ("#?", (2,), 1),
            ("?#", (2,), 1),
            ("??", (2,), 1),
            ("???.###", (1, 1, 3), 1),
            (".??..??...?##.", (1, 1, 3), 4),
            ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
            ("????.#...#...", (4, 1, 1), 1),
            ("????.######..#####.", (1, 6, 5), 4),
            ("?###????????", (3, 2, 1), 10),
            ("????#??.?.", (1, 2, 1), 7),
            ("???.???#???.??.#?.?", (1, 7, 1, 1), 9),
            ("??#??#????????", (2, 6), 3),
            ("?.#?", (1,), 1),
            (".????.#???#?#?#??.#?", (3, 1, 5, 1, 1), 4),
            ("???#???.???????????", (6, 6, 2), 12),
        ],
    )
    def test_example_by_line(self, record, counts, expected):
        print()
        assert calc(record, counts) == expected

    @pytest.mark.parametrize(
        ("record", "counts", "expected"),
        [
            ("???.###", (1, 1, 3), 1),
            (".??..??...?##.", (1, 1, 3), 16384),
            ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
            ("????.#...#...", (4, 1, 1), 16),
            ("????.######..#####.", (1, 6, 5), 2500),
            ("?###????????", (3, 2, 1), 506250),
            ("???#???.???????????", (6, 6, 2), 1920000),
        ],
    )
    def test_example_unfolded_by_line(self, record, counts, expected):
        print()
        assert (
            calc("?".join(record for _ in range(5)), tuple(list(counts) * 5))
            == expected
        )
