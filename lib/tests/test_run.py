from dataclasses import dataclass

import pytest

from .._helpers import DayPart
from ..run import _format_duration
from ..run import _get_selections
from ..run import Args


@pytest.mark.parametrize(
    ("duration_ns", "expected"),
    [
        (1, "1.0 ns"),
        (12, "12.0 ns"),
        (123, "123.0 ns"),
        (1_234, "1.2 μs"),
        (12_345, "12.3 μs"),
        (123_456, "123.5 μs"),
        (1_234_567, "1.2 ms"),
        (12_345_678, "12.3 ms"),
        (123_456_789, "123.5 ms"),
        (1_234_567_890, "1.2 s"),
        (12_345_678_901, "12.3 s"),
        (60_000_000_000, "1.0 min"),
        (72_000_000_000, "1.2 min"),
    ],
)
def test_format_duration(duration_ns: int, expected: str):
    assert _format_duration(duration_ns) == expected


@dataclass
class SelectionTestCase:
    all: list[DayPart]
    args: Args
    expected: list[DayPart]

    def __repr__(self) -> str:
        allstr = "" if self.all == default else f"{self.all!r}, "
        return f"{allstr}{self.args}"


default = list(map(lambda x: DayPart(*x), [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)]))

@pytest.mark.parametrize(
    "case",
    [
        SelectionTestCase([], Args(), []),
        SelectionTestCase(default, Args(), [DayPart(3, 1)]),
        SelectionTestCase(default, Args(parts=[1]), [DayPart(3, 1)]),
        SelectionTestCase(default, Args(parts=[1, 2]), [DayPart(3, 1)]),
        SelectionTestCase(default, Args(parts=[2]), []),
        SelectionTestCase(default, Args(days=[1]), [DayPart(1, 1), DayPart(1, 2)]),
        SelectionTestCase(default, Args(days=[2]), [DayPart(2, 1), DayPart(2, 2)]),
        SelectionTestCase(default, Args(days=[5]), []),
        SelectionTestCase(default, Args(days=[2, 3], parts=[1]), [DayPart(2, 1), DayPart(3, 1)]),
        SelectionTestCase(default, Args(days=[2, 3], parts=[1, 2]), [DayPart(2, 1), DayPart(2, 2), DayPart(3, 1)]),
        SelectionTestCase(default, Args(days=[2, 3], parts=[2]), [DayPart(2, 2)]),
        SelectionTestCase(default, Args(all=True), default),
        SelectionTestCase(default, Args(all=True, parts=[1]), [DayPart(1, 1), DayPart(2, 1), DayPart(3, 1)]),
        SelectionTestCase(default, Args(all=True, parts=[2]), [DayPart(1, 2), DayPart(2, 2)]),
        SelectionTestCase(default, Args(all=True, parts=[1, 2]), default),
    ],
    ids=repr,
)
def test_get_selections(case: SelectionTestCase):
    assert _get_selections(case.all, case.args) == case.expected
