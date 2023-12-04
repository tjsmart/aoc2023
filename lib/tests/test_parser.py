import pytest

from ..parser import collect_block_lines
from ..parser import collect_block_statements
from ..parser import collect_lines
from ..parser import Point


def test_collect_lines():
    s = """\
1 2
3 4
5 6
"""
    x = collect_lines(s, lambda x: tuple(map(int, x.split())))
    assert x == [(1, 2), (3, 4), (5, 6)]


def test_collect_lines_with_container():
    s = """\
1 2
3 4
5 6
"""
    x = collect_lines(s, lambda x: tuple(map(int, x.split())), dict)
    assert x == {1: 2, 3: 4, 5: 6}


def test_collect_block_lines():
    s = """\
1 2
3 4

5 6
7 8
"""
    x = collect_block_lines(s, lambda x: tuple(map(int, x.split())))
    assert x == [[(1, 2), (3, 4)], [(5, 6), (7, 8)]]


def test_collect_block_statements():
    s = """\
1 2
3 4

5 6
7 8
"""
    x = collect_block_statements(s, lambda x: tuple(map(int, x.split())))
    assert x == [(1, 2, 3, 4), (5, 6, 7, 8)]


def test_point_add():
    p = Point(1, 2)

    assert p + (3, 4) == (4, 6)
    assert p + 3 == (4, 5)

def test_point_sub():
    p = Point(1, 2)

    assert p - (1, 3) == (0, -1)
    assert p - 1 == (0, 1)

def test_point_mul():
    p = Point(1, 2)

    assert p * (3, 2) == (3, 4)
    assert p * 3 == (3, 6)

def test_point_floordiv():
    p = Point(3, 10)

    assert p // (4, 5) == (0, 2)
    assert p // 4 == (0, 2)

def test_point_mod():
    p = Point(3, 10)

    assert p % (4, 5) == (3, 0)
    assert p % 4 == (3, 2)


@pytest.mark.parametrize(
    'other', [(0, -2), (2, -2), (1, -1), (1, -3), (0, -1), (0, -3), (2, -1), (2, -3)], ids=repr
)
def test_is_adjacent_to_true_cases(other):
    p = Point(1, -2)
    assert p.is_adjacent_to(other)


@pytest.mark.parametrize(
    'other', [(1, -2), (-1, -2), (3, -2), (1, 0), (1, -4)], ids=repr
)
def test_is_adjacent_to_false_cases(other):
    p = Point(1, -2)
    assert not p.is_adjacent_to(other)


def test_iter_neighbors():
    p = Point(1, -2)
    expected_neighbors = {(0, -2), (2, -2), (1, -1), (1, -3), (0, -1), (0, -3), (2, -1), (2, -3)}

    observed_neighbors = set(p.iter_neighbors())
    assert observed_neighbors == expected_neighbors


def test_iter_neighbors_no_diagonals():
    p = Point(1, -2)
    expected_neighbors = {(0, -2), (2, -2), (1, -1), (1, -3)}

    observed_neighbors = set(p.iter_neighbors(diagonals=False))
    assert observed_neighbors == expected_neighbors
