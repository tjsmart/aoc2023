from __future__ import annotations

import operator
from collections.abc import Callable
from collections.abc import Iterable
from typing import NamedTuple
from typing import overload


@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
) -> list[T]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[tuple],
) -> tuple[T]:
    ...

@overload
def collect_lines[K, V](
    s: str,
    parser: Callable[[str], tuple[K, V]],
    container: type[dict],
) -> dict[K, V]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[set],
) -> set[T]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[tuple],
) -> tuple[T]:
    ...

@overload
def collect_lines[T](
    s: str,
    parser: Callable[[str], T],
    container: type[Iterable[T]],
) -> tuple[T]:
    ...

def collect_lines[T, U](
    s: str,
    parser: Callable[[str], T],
    container: Callable[[Iterable[T]], U] = list,
) -> U:
    return container(map(parser, s.splitlines()))


def collect_block_lines[T](
    s: str,
    parser: Callable[[str], T],
) -> list[list[T]]:
    return [collect_lines(block, parser) for block in s.split("\n\n")]


def collect_block_statements[T](
    s: str,
    parser: Callable[[str], T],
) -> list[T]:
    return [parser(block) for block in s.split("\n\n")]


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
