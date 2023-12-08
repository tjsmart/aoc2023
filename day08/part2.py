import math
from itertools import cycle


def solution(s: str) -> int:
    instructions_s, map_s = s.split('\n\n')
    map_ = dict(parse_line(line) for line in map_s.splitlines())

    ats = [k for k in map_ if k.endswith("A")]

    all_steps = []
    while ats:
        at = ats.pop()
        instructions = cycle(map(lambda x: {"L": 0, "R": 1}[x], instructions_s))
        steps = 0
        while not at.endswith("Z"):
            steps += 1
            instruction = next(instructions)
            at = map_[at][instruction]
        all_steps.append(steps)

    return math.lcm(*all_steps)


def parse_line(line: str) -> tuple[str, tuple[str, str]]:
    k, v_s = line.split(' = ')
    values = tuple(v_s[1:-1].split(', '))
    return k, values


class Test:
    import pytest

    EXAMPLE_INPUT = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    EXPECTED_RESULT = 6

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
