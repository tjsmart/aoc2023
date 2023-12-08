import math
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    duration: int


def solution(s: str) -> int:
    race = parse(s)
    first_root, last_root = calculate_roots(race)
    first = math.ceil(first_root)
    last = math.floor(last_root)
    return last - first + 1


def parse(s: str) -> Race:
    timestr, durationstr = s.splitlines()
    time = int("".join((map(str.strip, timestr.split(":")[1].strip().split()))))
    duration = int("".join((map(str.strip, durationstr.split(":")[1].strip().split()))))

    return Race(time, duration)


def calculate_roots(race: Race) -> tuple[float, float]:
    return (
        (race.time - math.sqrt(race.time**2 - 4 * race.duration)) / 2,
        (race.time + math.sqrt(race.time**2 - 4 * race.duration)) / 2,
    )


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
Time:   7 15  30
Distance: 9 40 200
""",
                71503,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
