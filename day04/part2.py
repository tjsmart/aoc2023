from dataclasses import dataclass
from typing import Self

from lib import collect_lines


@dataclass
class Card:
    count: int
    wn: set[int]
    mn: set[int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        _, nums = s.split(":")
        wns, mns = nums.split(" | ")
        wn = set(map(int, wns.strip().split()))
        mn = set(map(int, mns.strip().split()))
        return cls(1, wn, mn)

    def point_value(self) -> int:
        matches = self.wn & self.mn
        return len(matches)


def solution(s: str) -> int:
    cards = collect_lines(s, Card.from_str)

    for i, card in enumerate(cards):
        value = card.point_value()
        for j in range(1, value + 1):
            cards[i + j].count += card.count

    return sum(card.count for card in cards)


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3: 1 21 53 59 44 | 69 82 63 72 16 21 14 1
Card 4: 41 92 73 84 69 | 59 84 76 51 58 5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""",
                30,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
