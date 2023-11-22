import re
from dataclasses import dataclass

import pytest

from .._helpers import DayPart
from .._helpers import get_all_dayparts
from .._helpers import get_rootdir
from .._helpers import get_selections
from .._helpers import HandledError
from .._helpers import SelectionArgs


def test_daypart_next_raises_on_last_day():
    dp = DayPart(25, 2)

    with pytest.raises(HandledError) as ex:
        dp.next()

    assert "go home" in str(ex.value)


def test_daypart_next_returns_next_part():
    assert DayPart(13, 1).next() == (13, 2)

    assert DayPart(13, 2).next() == (14, 1)


def test_get_rootdir():
    get_rootdir.cache_clear()

    rootdir = str(get_rootdir())

    assert re.match(r'.*/aoc\d\d\d\d', rootdir)


@pytest.mark.usefixtures("rootdir")
def test_get_all_dayparts_empty():
    assert get_all_dayparts() == []


def test_get_all_dayparts(rootdir):
    (rootdir / "day01").mkdir()
    (rootdir / "day01" / "part1.py").touch()
    (rootdir / "day01" / "part2.py").touch()
    (rootdir / "day02").mkdir()
    (rootdir / "day02" / "part1.py").touch()
    (rootdir / "day03").mkdir()
    (rootdir / "day03" / "part2.py").touch()
    (rootdir / "day04").mkdir()

    assert get_all_dayparts() == [(1, 1), (1, 2), (2, 1), (3, 2)]


@dataclass
class SelectionTestCase:
    all: list[DayPart]
    args: SelectionArgs
    expected: list[DayPart]

    def __repr__(self) -> str:
        allstr = "" if self.all == default else f"{self.all!r}, "
        return f"{allstr}{self.args}"


default = list(map(lambda x: DayPart(*x), [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)]))

@pytest.mark.parametrize(
    "case",
    [
        SelectionTestCase([], SelectionArgs(), []),
        SelectionTestCase(default, SelectionArgs(), [DayPart(3, 1)]),
        SelectionTestCase(default, SelectionArgs(parts=[1]), [DayPart(3, 1)]),
        SelectionTestCase(default, SelectionArgs(parts=[1, 2]), [DayPart(3, 1)]),
        SelectionTestCase(default, SelectionArgs(parts=[2]), []),
        SelectionTestCase(default, SelectionArgs(days=[1]), [DayPart(1, 1), DayPart(1, 2)]),
        SelectionTestCase(default, SelectionArgs(days=[2]), [DayPart(2, 1), DayPart(2, 2)]),
        SelectionTestCase(default, SelectionArgs(days=[5]), []),
        SelectionTestCase(default, SelectionArgs(days=[2, 3], parts=[1]), [DayPart(2, 1), DayPart(3, 1)]),
        SelectionTestCase(default, SelectionArgs(days=[2, 3], parts=[1, 2]), [DayPart(2, 1), DayPart(2, 2), DayPart(3, 1)]),
        SelectionTestCase(default, SelectionArgs(days=[2, 3], parts=[2]), [DayPart(2, 2)]),
        SelectionTestCase(default, SelectionArgs(all=True), default),
        SelectionTestCase(default, SelectionArgs(all=True, parts=[1]), [DayPart(1, 1), DayPart(2, 1), DayPart(3, 1)]),
        SelectionTestCase(default, SelectionArgs(all=True, parts=[2]), [DayPart(1, 2), DayPart(2, 2)]),
        SelectionTestCase(default, SelectionArgs(all=True, parts=[1, 2]), default),
    ],
    ids=repr,
)
def test_get_selections(case: SelectionTestCase):
    assert get_selections(case.all, case.args) == case.expected
