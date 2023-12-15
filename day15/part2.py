from collections import defaultdict


def solution(s: str) -> int:
    steps = s.strip().split(",")
    boxes: dict[int, dict[str, int]] = defaultdict(dict)
    for step in steps:
        if "=" in step:
            label, _, fl = step.partition("=")
            fl = int(fl)
            bn = hashermasher(label)
            boxes[bn][label] = fl
        else:
            # must be '-'
            label = step[:-1]
            bn = hashermasher(label)
            boxes[bn].pop(label, None)

    total = 0
    for bn, box in boxes.items():
        for sn, fl in enumerate(box.values(), 1):
            total += focusing_power(bn, sn, fl)

    return total


def focusing_power(bn: int, sn: int, fl: int) -> int:
    return (bn + 1) * sn * fl


def hashermasher(step: str) -> int:
    h = 0
    for c in step:
        h += ord(c)
        h *= 17
        h %= 256

    return h


class Test:
    import pytest

    EXAMPLE_INPUT = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
    EXPECTED_RESULT = 145

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
