from __future__ import annotations

import operator
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from typing import NamedTuple
from typing import overload


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
    except TypeError:
        x, y = other, other # type: ignore

    try:
        return Point(operation(point.x, x), operation(point.y, y))
    except TypeError:
        raise TypeError(
            f"unsupported operand type(s) for {symbol}:"
            f" {type(point).__name__!r} and {type(other).__name__!r}"
        )

__all__ = [
    "collect_lines",
    "collect_block_lines",
    "collect_block_statements",
    "Point",
]
