from lib import collect_lines
from lib import Point


def solution(s: str) -> int:
    grid = collect_lines(s, list)

    rrs_seen: set[tuple[Point, ...]] = set()
    rrs: list[tuple[Point, ...]] = []
    start_recording = False
    offset = 0
    while rr := rolling_rocks(grid):
        if start_recording:
            if rr == rrs[0]:
                break

            rrs.append(rr)

        elif rr in rrs_seen:
            start_recording = True
            rrs.append(rr)

        else:
            rrs_seen.add(rr)
            offset += 1

        grid = cycle(grid)

    target = (1000000000 - offset) % len(rrs)
    return calc(rrs[target], len(grid))


def calc(rr: tuple[Point, ...], height: int) -> int:
    return sum(height - r.y for r in rr)


def rolling_rocks(grid: list[list[str]]) -> tuple[Point, ...]:
    return tuple(
        Point(x, y)
        for y in range(len(grid))
        for x in range(len(grid[0]))
        if grid[y][x] == "O"
    )


def cycle(g: list[list[str]]) -> list[list[str]]:
    # *north*, then *west*, then *south*, then *east*
    g = tilt_north(g)
    g = tilt_west(g)
    g = tilt_south(g)
    g = tilt_east(g)
    return g


def tilt_west(grid: list[list[str]]) -> list[list[str]]:
    tilted = []
    for row in grid:
        tilted.append([])
        for i, c in enumerate(row):
            if c == "O":
                tilted[-1].append(c)
            elif c in ("#", "X"):
                space = i - len(tilted[-1])
                tilted[-1].extend(["."] * space + [c])

        tilted[-1].extend(["."] * (len(row) - len(tilted[-1])))

    return tilted


def tilt_east(grid: list[list[str]]) -> list[list[str]]:
    tilted = []
    for row in grid:
        tilted.append([])
        for i, c in enumerate(reversed(row)):
            if c == "O":
                tilted[-1].insert(0, c)
            elif c in ("#", "X"):
                space = i - len(tilted[-1])
                tilted[-1][0:0] = [c] + ["."] * space

        tilted[-1][0:0] = ["."] * (len(row) - len(tilted[-1]))

    return tilted


def tilt_north(grid: list[list[str]]) -> list[list[str]]:
    t = transpose(grid)
    t = tilt_west(t)
    return transpose(t)


def tilt_south(grid: list[list[str]]) -> list[list[str]]:
    t = transpose(grid)
    t = tilt_east(t)
    return transpose(t)


def transpose(grid: list[list[str]]) -> list[list[str]]:
    return [[grid[y][x] for y in range(len(grid))] for x in range(len(grid[0]))]


def print_grid(grid: list[list[str]]) -> None:
    print("\n" + "\n".join("".join(c for c in row) for row in grid))


class Test:
    import pytest

    EXAMPLE_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    EXPECTED_RESULT = 64

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
