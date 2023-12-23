from collections import deque

from lib import FrozenGrid
from lib import Point


def solution(s: str) -> int:
    grid = FrozenGrid.from_str(s)
    start = Point(1, 0)
    end = Point(grid.col_len() - 2, grid.row_len() - 1)
    queue: deque[tuple[Point, set[Point]]] = deque([(start, set())])
    best = 0
    while queue:
        loc, been = queue.popleft()

        for i, (_, other) in reversed(list(enumerate(queue))):
            if loc in other:
                del queue[i]

        for n in loc.iter_neighbors(diagonals=False):
            if n in been or ((c := grid[n.y][n.x]) == "#"):
                continue

            if n == end:
                been.add(loc)
                best = max(best, len(been))
                break

            if grid.on_edge(n):
                continue

            match c:
                case ".":
                    queue.append((n, been | {loc}))
                case ">":
                    if n - loc == (-1, 0):
                        continue
                    queue.append((n + (1, 0), been | {loc, n}))
                case "v":
                    if n - loc == (0, -1):
                        continue
                    queue.append((n + (0, 1), been | {loc, n}))
                case _:
                    raise ValueError(f"Invalid tile: {c}")

    return best


class Test:
    import pytest

    EXAMPLE_INPUT = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
    EXPECTED_RESULT = 94

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
