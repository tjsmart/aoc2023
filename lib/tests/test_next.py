import os
from functools import partial
from unittest.mock import patch

import pytest

from .. import next


patch_mut = partial(patch.object, next)


@pytest.fixture
def mock_input():
    with patch_mut("_get_input") as mock:
        mock.return_value = "input\nyeah!"
        yield mock.return_value


@pytest.fixture
def mock_prompt():
    with patch_mut("_get_prompt") as mock:
        mock.return_value = "# AOC prompt\nyeah!"
        yield mock.return_value


@pytest.fixture(autouse=True)
def mock_open():
    with patch_mut("_open"):
        yield


def test_next_can_create_first_thing(rootdir, mock_input, mock_prompt):
    next._main()

    nextfile = rootdir / "day01" / "part1.py"
    assert nextfile.exists()
    assert "def solution" in nextfile.read_text()

    nextfile = rootdir / "day01" / "__init__.py"
    assert nextfile.exists()
    assert nextfile.read_text() == ""

    nextfile = rootdir / "day01" / "input.txt"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_input

    nextfile = rootdir / "day01" / "prompt.md"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_prompt


def test_next_can_create_part1(rootdir, mock_input, mock_prompt):
    (rootdir / "day12").mkdir()
    (rootdir / "day12" / "part2.py").write_text("day12 part2 contents")

    next._main()

    nextfile = rootdir / "day13" / "part1.py"
    assert nextfile.exists()
    assert "def solution" in nextfile.read_text()

    nextfile = rootdir / "day13" / "__init__.py"
    assert nextfile.exists()
    assert nextfile.read_text() == ""

    nextfile = rootdir / "day13" / "input.txt"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_input

    nextfile = rootdir / "day13" / "prompt.md"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_prompt


def test_next_can_create_part2(rootdir, mock_prompt):
    (rootdir / "day12").mkdir()
    (rootdir / "day12" / "part1.py").write_text("part1 contents")

    next._main()

    nextfile = rootdir / "day12" / "part2.py"
    assert nextfile.exists()
    assert nextfile.read_text() == "part1 contents"

    nextfile = rootdir / "day12" / "prompt.md"
    assert nextfile.exists()
    assert nextfile.read_text() == mock_prompt


# def test_get_input():
#     # https://adventofcode.com/2015/day/4/input
#     rslt = next._get_input(year=2015, day=4)
#     assert rslt == "iwrupvqb"
