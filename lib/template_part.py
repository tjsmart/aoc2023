from lib import collect_lines


def solution(s: str) -> int:
    return sum(collect_lines(s, parse))


def parse(s: str) -> int:
    ...

class Test:
    import pytest

    @pytest.mark.parametrize(
            ("case", "expected"),
            [
                ("""\
""", 123),
                ],
            )
    def test_examples(self, case, expected):
        assert solution(case) == expected
