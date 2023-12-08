from dataclasses import dataclass

from lib import collect_lines


def solution(s: str) -> int:
    things = collect_lines(s, Thing.from_str)


class Test:
    import pytest

    EXAMPLE_INPUT = """\
"""
    EXPECTED_RESULT = 0

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
