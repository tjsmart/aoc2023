from dataclasses import dataclass
from typing import Self

from lib import collect_lines


type grab = dict[str, int]


CUBES_AVAILABLE = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def solution(s: str) -> int:
    games = collect_lines(s, Game.from_str)
    return sum(game.ID for game in games if game.is_valid())


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

    def is_valid(self) -> bool:
        for grab in self.grabs:
            for color, count in grab.items():
                if CUBES_AVAILABLE.get(color, 0) < count:
                    return False
        return True


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
                8,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
