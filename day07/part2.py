from collections import Counter
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from enum import auto
from enum import IntEnum
from typing import Self

from lib import collect_lines


card_name_to_value = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
        "J": 0,
}


@dataclass(order=True)
class Hand:
    cards: list[int]
    bid: int = field(compare=False)

    @classmethod
    def from_str(cls, s: str) -> Self:
        cards_s, bid_s = s.split()
        cards = [card_name_to_value[name] for name in cards_s]
        bid = int(bid_s)
        return cls(cards, bid)


class Score(IntEnum):
    HIGH_CAR = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


def solution(s: str) -> int:
    hands = collect_lines(s, Hand.from_str)
    scores = [(score(hand), hand) for hand in hands]
    scores.sort()
    return sum(i * hand.bid for i, (_, hand) in enumerate(scores, 1))

def score(hand: Hand) -> Score:
    unique = Counter(hand.cards)

    J = card_name_to_value["J"]

    if unique == {J: 5}:
        unique = {card_name_to_value["K"]: 5}

    elif J in unique:
        counts = defaultdict(list)
        for card, count in unique.items():
            counts[count].append(card)

        max_count = max(counts)
        if counts[max_count] == [J]:
            counts.pop(max_count)
            max_count = max(counts)

        letter_to_pretend_to_be = max(counts[max_count])
        unique[letter_to_pretend_to_be] += unique.pop(J)

    match len(unique):
        case 1:
            return Score.FIVE_OF_A_KIND
        case 2:
            if set(unique.values()) == {4, 1}:
                return Score.FOUR_OF_A_KIND
            if set(unique.values()) == {3, 2}:
                return Score.FULL_HOUSE
        case 3:
            if set(unique.values()) == {3, 1, 1}:
                return Score.THREE_OF_A_KIND
            if set(unique.values()) == {2, 2, 1}:
                return Score.TWO_PAIR
        case 4:
            return Score.ONE_PAIR
        case 5:
            return Score.HIGH_CAR

    assert False, f"Unexpected: {unique}"


class Test:
    import pytest

    @pytest.mark.parametrize(
            ("case", "expected"),
            [
                ("""\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""", 5905),
                ],
            )
    def test_examples(self, case, expected):
        assert solution(case) == expected
