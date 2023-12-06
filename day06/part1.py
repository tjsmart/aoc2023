from collections.abc import Iterable
from dataclasses import dataclass

from lib import collect_lines

@dataclass
class Race:
    time: int
    duration: int




def solution(s: str) -> int:
    races = parse(s)
    return product(map(number_of_ways_to_win, races))


def parse(s: str) -> list[Race]:
    timestr, durationstr = s.splitlines()
    times = list(map(int, timestr.split(':')[1].strip().split()))
    durations = list(map(int, durationstr.split(':')[1].strip().split()))

    return [Race(time, duration) for time, duration in zip(times, durations)]

def number_of_ways_to_win(race: Race) -> int:
    i = 1
    ways = 0
    while True:
        if calculate_distance(race, i) > race.duration:
            ways += 1
        elif ways:
            return ways

        i += 1


def calculate_distance(race: Race, speed: int) -> int:
    dt = race.time - speed
    return speed * dt


def product(values: Iterable[int]) -> int:
    p = 1
    for value in values:
        p *= value
    return p

class Test:
    import pytest

    @pytest.mark.parametrize(
            ("case", "expected"),
            [
                ("""\
Time:   7 15  30
Distance: 9 40 200
""", 288),
                ],
            )
    def test_examples(self, case, expected):
        assert solution(case) == expected
