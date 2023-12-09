import itertools

from lib import collect_lines


def solution(s: str) -> int:
    histories = collect_lines(s, lambda line: [int(x) for x in line.split()])
    return sum(predict(history) for history in histories)


def predict(history: list[int]) -> int:
    diffs = history
    ends = []
    while not all(diff == diffs[0] for diff in diffs):
        ends.append(diffs[-1])
        diffs = [y - x for x, y in itertools.pairwise(diffs)]

    ends.append(diffs[-1])
    return sum(ends)


class Test:
    import pytest

    EXAMPLE_INPUT = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    EXPECTED_RESULT = 114

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
