from lib import collect_lines

numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def solution(s: str) -> int:
    return sum(collect_lines(s, parse))


def parse(line: str) -> int:
    first = find_first(line)
    last = find_last(line)
    return int(str(first) + str(last))


def find_first(s: str) -> int:
    first_idx = len(s)
    first_value = None
    for name, value in numbers.items():
        idx_name = s.find(name)
        idx_value = s.find(str(value))
        if idx_name == -1 and idx_value == -1:
            continue
        if idx_name == -1:
            idx = idx_value
        elif idx_value == -1:
            idx = idx_name
        else:
            idx = min(idx_name, idx_value)

        if idx < first_idx:
            first_idx = idx
            first_value = value

    assert first_value is not None,s

    return first_value


def find_last(s: str) -> int:
    last_idx = -1
    last_value = None
    for name, value in numbers.items():
        idx_name = s.rfind(name)
        idx_value = s.rfind(str(value))
        if idx_name == -1 and idx_value == -1:
            continue
        if idx_name == -1:
            idx = idx_value
        elif idx_value == -1:
            idx = idx_name
        else:
            idx = max(idx_name, idx_value)

        if idx > last_idx:
            last_idx = idx
            last_value = value

    assert last_value is not None, s

    return last_value




class Test:
    import pytest

    @pytest.mark.parametrize(
            ("case", "expected"),
            [
                ("two1nine", 29),
                ("eightwothree", 83),
                ("abcone2threexyz", 13),
                ("xtwone3four", 24),
                ("4nineeightseven2", 42),
                ("zoneight234", 14),
                ("7pqrstsixteen",76),
                (
                    """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""", 281),
                ("one",11),
                ("two",22),
                ("three",33),
                ("four",44),
                ("five",55),
                ("six",66),
                ("seven",77),
                ("eight",88),
                ("nine",99),
                ("1",11),
                ("2",22),
                ("3",33),
                ("4",44),
                ("5",55),
                ("6",66),
                ("7",77),
                ("8",88),
                ("9",99),
                ("98765",95),
                ("1989",19),
                ],
            )
    def test_examples(self, case, expected):
        assert solution(case) == expected
