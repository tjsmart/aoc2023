from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from lib import collect_lines


type grab = dict[str, int]


def solution(s: str) -> int:
    games = collect_lines(s, Game.from_str)
    return sum(game.get_power() for game in games)


@dataclass
class Game:
    ID: int
    grabs: list[grab]

    @classmethod
    def from_str(cls, s) -> Self:
        game_str, s = s.split(":")
        ID = int(game_str.split()[1])
        grabs = list(map(parse_grab, s.split(";")))
        return cls(ID, grabs)

    def get_power(self) -> int:
        min_required = defaultdict(int)
        for grab in self.grabs:
            for color, count in grab.items():
                if min_required[color] < count:
                    min_required[color] = count

        return min_required["red"] * min_required["blue"] * min_required["green"]


def parse_grab(s: str) -> grab:
    grab = {}
    for x in s.split(","):
        count, color = x.strip().split()
        grab[color] = int(count)
    return grab


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""",
                2286,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
