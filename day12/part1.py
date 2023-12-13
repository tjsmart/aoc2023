import itertools

from lib import collect_lines


def solution(s: str) -> int:
    readings = collect_lines(s, parse)
    return sum(map(calc, readings))


def calc(reading: tuple[str, tuple[int, ...]]) -> int:
    record, ds = reading
    uds = sum(ds) - record.count('#')
    qids = [i for i in range(len(record)) if record[i] == '?']

    ars = 0
    for rids in itertools.combinations(qids, uds):
        ars += check_if_matches_target(record, ds, rids)
    return ars


def check_if_matches_target(record: str, ds: tuple[int, ...], rids: tuple[int, ...]) -> bool:
    targets = list(reversed(ds))
    group = 0
    for i, c in enumerate(record):
        if i in rids or c == '#':
            if not targets:
                return False
            group += 1
        else:
            if group and group != try_pop(targets):
                return False

            group = 0

    if group and group != try_pop(targets):
        return False

    return True


def try_pop(x: list[int]) -> int | None:
    try:
        return x.pop()
    except IndexError:
        return None


def parse(line: str) -> tuple[str, tuple[int, ...]]:
    x, y = line.split()
    return x, tuple(map(int, y.strip().split(',')))


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
    EXPECTED_RESULT = 21

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected


    @pytest.mark.parametrize(
        ("case", "expected"),
        [
(("???.###", (1,1,3)), 1),
((".??..??...?##.", (1,1,3)), 4),
(("?#?#?#?#?#?#?#?", (1,3,1,6)), 1),
(("????.#...#...", (4,1,1)), 1),
(("????.######..#####.", (1,6,5)), 4),
(("?###????????", (3,2,1)), 10),
        ],
    )
    def test_example_by_line(self, case, expected):
        assert calc(case) == expected
