from __future__ import annotations

import operator
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from dataclasses import dataclass
from typing import final
from typing import NamedTuple
from typing import overload
from typing import SupportsIndex


@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    *,
    debug: bool = False,
) -> list[T]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[tuple],
    *,
    debug: bool = False,
) -> tuple[T]:
    ...

@overload
def collect_lines[K, V](
    s: str,
    parser: Callable[[str], tuple[K, V]],
    container: type[dict],
    *,
    debug: bool = False,
) -> dict[K, V]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[set],
    *,
    debug: bool = False,
) -> set[T]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[tuple],
    *,
    debug: bool = False,
) -> tuple[T]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[Iterable[T]],
    *,
    debug: bool = False,
) -> tuple[T]:
    ...

def collect_lines[T, U](
    s: str,
    parser: Callable[[str], T],
    container: Callable[[Iterable[T]], U] = list,
    *,
    debug: bool = False,
) -> U:
    if debug:
        def parser_used(s: str, /) -> T:
            rslt = parser(s)
            print(f"{s} -> {rslt}")
            return rslt
    else:
        parser_used = parser

    return container(map(parser_used, s.splitlines()))


def collect_block_lines[T](
    s: str,
    parser: Callable[[str], T],
    *,
    debug: bool = False,
) -> list[list[T]]:
    if debug:
        def collect_lines_used(block: str, parser: Callable[[str], T], /) -> list[T]:
            rslt = collect_lines(block, parser, debug=debug)
            print(f"block -> {rslt}")
            return rslt
    else:
        collect_lines_used = collect_lines

    return [collect_lines_used(block, parser) for block in s.split("\n\n")]


def collect_block_statements[T](
    s: str,
    parser: Callable[[str], T],
    *,
    debug: bool = False,
) -> list[T]:
    if debug:
        def parser_used(block: str, /) -> T:
            rslt = parser(block)
            print(f"{block}\n  gives: {rslt}")
            return rslt
    else:
        parser_used = parser

    return [parser_used(block) for block in s.split("\n\n")]


class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other: tuple[int, int] | int) -> Point:
        return _point_operation(self, other, operator.add, "+")

    def __sub__(self, other: tuple[int, int] | int) -> Point:
        return _point_operation(self, other, operator.sub, "-")

    def __mul__(self, other: tuple[int, int] | int) -> Point:
        return _point_operation(self, other, operator.mul, "*")

    # def __div__(self, other: tuple[int, int] | int) -> Point:
    #     return _point_operation(self, other, operator.truediv, "/")

    def __floordiv__(self, other: tuple[int, int] | int) -> Point:
        return _point_operation(self, other, operator.floordiv, "//")

    def __mod__(self, other: tuple[int, int] | int) -> Point:
        return _point_operation(self, other, operator.mod, "%")

    def is_adjacent_to(self, other: tuple[int, int]) -> bool:
        dx = self.x - other[0]
        dy = self.y - other[1]
        return bool(dx or dy) and abs(dx) <= 1 and abs(dy) <= 1

    def iter_neighbors(self, diagonals: bool = True) -> Iterator[Point]:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not diagonals and abs(dx) == abs(dy) == 1:
                    continue
                if dx == dy == 0:
                    continue
                yield self + (dx, dy)

def _point_operation(
    point: Point,
    other: tuple[int, int] | int,
    operation: Callable[[int, int], int],
    symbol: str,
) -> Point:
    x: int
    y: int
    try:
        x, y = other  # type: ignore
    except (ValueError, TypeError):
        x, y = other, other # type: ignore

    try:
        return Point(operation(point.x, x), operation(point.y, y))
    except TypeError:
        raise TypeError(
            f"unsupported operand type(s) for {symbol}:"
            f" {type(point).__name__!r} and {type(other).__name__!r}"
        )



@final
@dataclass(frozen=True)
class FrozenGrid[T](Sequence[Sequence[T]]):
    type Array = tuple[T, ...]
    _grid: tuple[Array, ...]

    def iter_rows(self) -> Iterator[Array]:
        yield from self._grid

    def iter_rev_rows(self) -> Iterator[Array]:
        yield from reversed(self._grid)

    def iter_cols(self) -> Iterator[Array]:
        yield from zip(*self._grid)

    def iter_rev_cols(self) -> Iterator[Array]:
        yield from reversed(tuple(zip(*self._grid)))

    def iter_values(self) -> Iterator[T]:
        return (c for row in self for c in row)

    def enum_rows(self) -> Iterator[tuple[int, Array]]:
        yield from enumerate(self.iter_rows())

    def enum_cols(self) -> Iterator[tuple[int, Array]]:
        yield from enumerate(self.iter_cols())

    def enum_values(self) -> Iterator[tuple[Point, T]]:
        return ((Point(x, y), self[y][x]) for y in range(self.row_len()) for x in range(self.col_len()))

    def row_len(self) -> int:
        return len(self)

    def col_len(self) -> int:
        return len(self[0])


    @overload
    def __getitem__(self, __key: SupportsIndex) -> Array:
        ...

    @overload
    def __getitem__(self, __key: tuple[int, int]) -> T:
        ...

    def __getitem__(self, __key: SupportsIndex | tuple[int, int]) -> Array | T:
        try:
            k = operator.index(__key) # type: ignore
        except TypeError:
            x, y = __key  # type: ignore
            return self[y][x]
        else:
            return self._grid[k]

    def __len__(self) -> int:
        return len(self._grid)

    @classmethod
    def from_iter(cls, grid: Iterable[Iterable[T]], /) -> FrozenGrid[T]:
        return cls(tuple(tuple(row) for row in grid))

    @overload
    @classmethod
    def from_str(cls, s: str) -> FrozenGrid[str]:
        ...

    @overload
    @classmethod
    def from_str(cls, s: str, p: Callable[[str], T]) -> FrozenGrid[T]:
        ...

    @classmethod
    def from_str(cls, s: str, p: Callable[[str], T] |  None = None) -> FrozenGrid[T] | FrozenGrid[str]:
        if p is None:
            x = collect_lines(s, list)
            return cls.from_iter(x)
        else:
            x = collect_lines(s, lambda x: list(map(p, x)))
            return cls.from_iter(x)

    def __repr__(self) -> str:
        return '\n'.join("".join(str(c) for c in row) for row in self)

    def transpose(self) -> FrozenGrid:
        return FrozenGrid.from_iter(self.iter_cols())

    def rotate(self, turns: int) -> FrozenGrid:
        """rotate grid by 90° turns, +/- turns corresponds to ccw/cw rotation"""
        match turns % 4:
            case 0:
                return FrozenGrid(self._grid)
            case 1 | -3:
                return FrozenGrid.from_iter(self.iter_rev_cols())
            case 2 | -2:
                return FrozenGrid.from_iter(reversed(row) for row in reversed(self))
            case 3 | -1:
                return FrozenGrid.from_iter(zip(*reversed(self._grid)))

        raise TypeError(f"Invalid turns: {turns}")

    def hreflect(self) -> FrozenGrid:
        return FrozenGrid.from_iter(reversed(row) for row in self._grid)

    def vreflect(self) -> FrozenGrid:
        return FrozenGrid.from_iter(self.iter_rev_rows())

    def in_bounds(self, p: Point) -> bool:
        return 0 <= p.x < self.col_len() and 0 <= p.y < self.row_len()

    def on_edge(self, p: Point) -> bool:
        return (
            p.y <= 0
            or p.x <= 0
            or p.y >= self.row_len() - 1
            or p.x >= self.col_len() - 1
        )

    def find(self, t: T, /) -> Point:
        for y, row in self.enum_rows():
            for x, c in enumerate(row):
                if c == t:
                    return Point(x, y)
        raise ValueError(f"value {t!r} not located in grid")


__all__ = [
    "collect_lines",
    "collect_block_lines",
    "collect_block_statements",
    "Point",
    "FrozenGrid",
]
