from .part2 import calc
from lib import collect_lines


def solution(s: str) -> int:
    readings = collect_lines(s, parse)
    return sum(map(lambda reading: calc(*reading), readings))


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
            (("???.###", (1, 1, 3)), 1),
            ((".??..??...?##.", (1, 1, 3)), 4),
            (("?#?#?#?#?#?#?#?", (1, 3, 1, 6)), 1),
            (("????.#...#...", (4, 1, 1)), 1),
            (("????.######..#####.", (1, 6, 5)), 4),
            (("?###????????", (3, 2, 1)), 10),
        ],
    )
    def test_example_by_line(self, case, expected):
        assert calc(case) == expected
