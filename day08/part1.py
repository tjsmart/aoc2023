from dataclasses import dataclass
from itertools import cycle

from lib import collect_lines



def solution(s: str) -> int:
    instructions_s, map_s = s.split('\n\n')
    instructions = cycle(map(lambda x: {"L": 0, "R": 1}[x], instructions_s))
    map_ = dict(parse_line(line) for line in map_s.splitlines())

    at = "AAA"
    steps = 0
    while at != "ZZZ":
        steps += 1
        instruction = next(instructions)
        at = map_[at][instruction]

    return steps


def parse_line(line: str) -> tuple[str, tuple[str, str]]:
    k, v_s = line.split(' = ')
    values = tuple(v_s[1:-1].split(', '))
    return k, values

class Test:
    import pytest

    EXAMPLE_INPUT = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
    EXPECTED_RESULT = 2

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
            ("""\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""", 6),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
