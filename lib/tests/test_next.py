import os
import re
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from .. import next


patch_mut = partial(patch.object, next)


@pytest.fixture
def rootdir():
    startingdir = Path.cwd()
    with patch_mut("_get_rootdir") as mock_get_rootdir, TemporaryDirectory() as tempd:
        rootdir = Path(tempd) / "aoc1994"
        rootdir.mkdir(exist_ok=True, parents=True)
        mock_get_rootdir.return_value = rootdir
        os.chdir(rootdir)
        yield rootdir

    os.chdir(startingdir)


@pytest.fixture
def mock_input():
    with patch_mut("_get_input") as mock:
        mock.return_value = "input\nyeah!"
        yield mock.return_value


@pytest.fixture(autouse=True)
def mock_os_execlp():
    with patch.object(os, "execlp"):
        yield


def test_next_can_first_thing(rootdir, mock_input):
    next._main()

    nextfile = rootdir / "day01" / "part1.py"
    assert nextfile.exists()
    assert "def main" in nextfile.read_text()

    nextfile = rootdir / "day01" / "__init__.py"
    assert nextfile.exists()
    assert nextfile.read_text() == ""

    nextfile = rootdir / "day01" / "input.txt"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_input


def test_next_can_create_part1(rootdir, mock_input):
    (rootdir / "day12").mkdir()
    (rootdir / "day12" / "part2.py").write_text("day12 part2 contents")

    next._main()

    nextfile = rootdir / "day13" / "part1.py"
    assert nextfile.exists()
    assert nextfile.read_text() == "day12 part2 contents"

    nextfile = rootdir / "day13" / "__init__.py"
    assert nextfile.exists()
    assert nextfile.read_text() == ""

    nextfile = rootdir / "day13" / "input.txt"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_input


def test_next_can_create_part2(rootdir):
    (rootdir / "day12").mkdir()
    (rootdir / "day12" / "part1.py").write_text("part1 contents")

    next._main()

    nextfile = rootdir / "day12" / "part2.py"
    assert nextfile.exists()
    assert nextfile.read_text() == "part1 contents"


def test_get_rootdir():
    next._get_rootdir.cache_clear()

    rootdir = str(next._get_rootdir())

    assert re.match(r'.*/aoc\d\d\d\d', rootdir)


# def test_get_input():
#     # https://adventofcode.com/2015/day/4/input
#     rslt = next._get_input(year=2015, day=4)
#     assert rslt == "iwrupvqb"
