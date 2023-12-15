def solution(s: str) -> int:
    return sum(hashermasher(step) for step in s.strip().split(","))


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
    EXPECTED_RESULT = 1320

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
            ("HASH", 52),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
