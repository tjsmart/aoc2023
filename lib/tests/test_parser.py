import pytest

from ..parser import collect_block_lines
from ..parser import collect_block_statements
from ..parser import collect_lines
from ..parser import FrozenGrid
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
    "other",
    [(0, -2), (2, -2), (1, -1), (1, -3), (0, -1), (0, -3), (2, -1), (2, -3)],
    ids=repr,
)
def test_is_adjacent_to_true_cases(other):
    p = Point(1, -2)
    assert p.is_adjacent_to(other)


@pytest.mark.parametrize(
    "other", [(1, -2), (-1, -2), (3, -2), (1, 0), (1, -4)], ids=repr
)
def test_is_adjacent_to_false_cases(other):
    p = Point(1, -2)
    assert not p.is_adjacent_to(other)


def test_iter_neighbors():
    p = Point(1, -2)
    expected_neighbors = {
        (0, -2),
        (2, -2),
        (1, -1),
        (1, -3),
        (0, -1),
        (0, -3),
        (2, -1),
        (2, -3),
    }

    observed_neighbors = set(p.iter_neighbors())
    assert observed_neighbors == expected_neighbors


def test_iter_neighbors_no_diagonals():
    p = Point(1, -2)
    expected_neighbors = {(0, -2), (2, -2), (1, -1), (1, -3)}

    observed_neighbors = set(p.iter_neighbors(diagonals=False))
    assert observed_neighbors == expected_neighbors


def test_is_hashable():
    g = ((1, 2), (3, 4))
    assert len({FrozenGrid(g), FrozenGrid(g)}) == 1


def test_iterable():
    g = ((1, 2), (3, 4))
    for act, exp in zip(FrozenGrid(g), g):
        assert act == exp


def test_iterable_iterable():
    g = ((1, 2), (3, 4))
    for act, exp in zip(FrozenGrid(g), g):
        for a, e in zip(act, exp):
            assert a == e


def test_len():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    assert len(g) == 3
    assert g.row_len() == 3
    assert g.col_len() == 2


def test_iter_rows():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    assert list(g.iter_rows()) == [(1, 2), (3, 4), (5, 6)]


def test_iter_rev_rows():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    assert list(g.iter_rev_rows()) == [(5, 6), (3, 4), (1, 2)]


def test_iter_cols():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    assert list(g.iter_cols()) == [(1, 3, 5), (2, 4, 6)]


def test_iter_rev_cols():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    assert list(g.iter_rev_cols()) == [(2, 4, 6), (1, 3, 5)]


def test_rotate_ccw_1():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12
    34   ->   246
    56        135
    """
    assert g.rotate(1) == FrozenGrid(((2, 4, 6), (1, 3, 5)))


def test_rotate_ccw_2():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12                   65
    34   ->   246   ->   43
    56        135        21
    """
    assert g.rotate(2) == FrozenGrid(((6, 5), (4, 3), (2, 1)))


def test_rotate_ccw_3():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12                   65
    34   ->   246   ->   43   ->  531
    56        135        21       642
    """
    assert g.rotate(3) == FrozenGrid(((5, 3, 1), (6, 4, 2)))


def test_rotate_ccw_4():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12                   65                12
    34   ->   246   ->   43   ->  531  ->  34
    56        135        21       642      56
    """
    assert g.rotate(4) == FrozenGrid(((1, 2), (3, 4), (5, 6)))


def test_rotate_cw_1():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12
    34   ->   531
    56        642
    """
    assert g.rotate(-1) == FrozenGrid(((5, 3, 1), (6, 4, 2)))


def test_rotate_cw_2():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12                 65
    34   ->   531  ->  43
    56        642      21
    """
    assert g.rotate(-2) == FrozenGrid(((6, 5), (4, 3), (2, 1)))


def test_rotate_cw_3():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12                 65
    34   ->   531  ->  43  ->  246
    56        642      21      135
    """
    assert g.rotate(-3) == FrozenGrid(((2, 4, 6), (1, 3, 5)))


def test_rotate_cw_4():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12                 65               12
    34   ->   531  ->  43  ->  246  ->  34
    56        642      21      135      56
    """
    assert g.rotate(-4) == FrozenGrid(((1, 2), (3, 4), (5, 6)))


def test_vreflect():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12        56
    34   ->   34
    56        12
    """
    assert g.vreflect() == FrozenGrid(((5, 6), (3, 4), (1, 2)))


def test_hreflect():
    g = FrozenGrid(((1, 2), (3, 4), (5, 6)))
    """
    12        21
    34   ->   43
    56        65
    """
    assert g.hreflect() == FrozenGrid(((2, 1), (4, 3), (6, 5)))
