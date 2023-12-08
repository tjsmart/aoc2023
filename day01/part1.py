from lib import collect_lines


def solution(s: str) -> int:
    return sum(collect_lines(s, parse))


def parse(line: str) -> int:
    first = find_first(line)
    last = find_last(line)
    return int(str(first) + str(last))


def find_first(s: str) -> int:
    for x in s:
        try:
            return int(x)
        except ValueError:
            pass

    assert False


def find_last(s: str) -> int:
    for x in reversed(s):
        try:
            return int(x)
        except ValueError:
            pass

    assert False


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [("1abc2", 12), ("pqr3stu8vwx", 38), ("a1b2c3d4e5f", 15), ("treb7uchet", 77)],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
