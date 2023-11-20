import re

import pytest

from .._helpers import DayPart
from .._helpers import get_all_dayparts
from .._helpers import get_rootdir
from .._helpers import HandledError


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
