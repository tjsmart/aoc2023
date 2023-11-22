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
