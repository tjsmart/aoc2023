from collections import defaultdict
from collections import deque
from typing import NamedTuple

from lib import FrozenGrid
from lib import Inf
from lib import InfType
from lib import Point


class Node(NamedTuple):
    loc: Point
    dir: Point
    slc: int
    hls: int


def solution(s: str) -> int:
    grid = FrozenGrid.from_str(s, int)

    queue: deque[Node] = deque(
        [
            Node(Point(1, 0), Point(1, 0), 1, 0),
            Node(Point(0, 1), Point(0, 1), 1, 0),
        ]
    )
    visited: dict[tuple[Point, Point, int], int | InfType] = defaultdict(InfType)
    min_hls = Inf
    while queue:
        node = queue.popleft()

        if visited[(node.loc, node.dir, node.slc)] < node.hls:
            continue

        if node.hls >= min_hls:
            continue

        hls_at_loc = grid[node.loc.y][node.loc.x]
        candidates = get_candidates(node, hls_at_loc)
        for c in candidates:
            if c.loc.y == grid.row_len() - 1 and c.loc.x == grid.col_len() - 1:
                min_hls = min(min_hls, c.hls)
                continue

            if not grid.in_bounds(c.loc):
                continue

            if visited[(c.loc, c.dir, c.slc)] <= c.hls:
                continue

            visited[(c.loc, c.dir, c.slc)] = c.hls
            queue.append(c)

    assert not isinstance(min_hls, InfType)

    return min_hls + grid[-1][-1]


def get_candidates(node: Node, hls_at_loc: int) -> list[Node]:
    def create_node(dir: tuple[int, int], slc: int) -> Node:
        return Node(
            node.loc + dir,
            Point(*dir),
            slc,
            node.hls + hls_at_loc,
        )

    match node.dir, node.slc:
        case (Point(1, 0), 3):
            return [
                create_node((0, 1), 1),
                create_node((0, -1), 1),
            ]
        case (Point(1, 0), _):
            return [
                create_node((0, 1), 1),
                create_node((0, -1), 1),
                create_node((1, 0), node.slc + 1),
            ]

        case (Point(-1, 0), 3):
            return [
                create_node((0, 1), 1),
                create_node((0, -1), 1),
            ]
        case (Point(-1, 0), _):
            return [
                create_node((0, 1), 1),
                create_node((0, -1), 1),
                create_node((-1, 0), node.slc + 1),
            ]

        case (Point(0, 1), 3):
            return [
                create_node((1, 0), 1),
                create_node((-1, 0), 1),
            ]
        case (Point(0, 1), _):
            return [
                create_node((1, 0), 1),
                create_node((-1, 0), 1),
                create_node((0, 1), node.slc + 1),
            ]

        case (Point(0, -1), 3):
            return [
                create_node((1, 0), 1),
                create_node((-1, 0), 1),
            ]
        case (Point(0, -1), _):
            return [
                create_node((1, 0), 1),
                create_node((-1, 0), 1),
                create_node((0, -1), node.slc + 1),
            ]

    assert False, "uh oh! 😲"


class Test:
    import pytest

    EXAMPLE_INPUT = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
    EXPECTED_RESULT = 102

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
