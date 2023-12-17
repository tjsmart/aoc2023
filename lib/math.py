from __future__ import annotations

import math
from collections.abc import Iterable
from functools import total_ordering
from typing import final
from typing import Literal
from typing import overload

from ._helpers import Singleton


def solve_quadratic(a: float, b: float, c: float) -> tuple[float, float]:
    return (
        (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a),
        (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a),
    )


@overload
def product(values: Iterable[int], default: int = 1) -> int:
    ...


@overload
def product(values: Iterable[float], default: float = 1) -> float:
    ...


def product(values: Iterable[float], default: float = 1) -> float:
    p = default
    for value in values:
        p *= value
    return p


@final
@total_ordering
class InfType(Singleton):
    """
    Positive infinity
    """

    def __repr__(self) -> str:
        return "Inf"

    @overload
    def __gt__(self, other: int) -> Literal[True]:
        ...

    @overload
    def __gt__(self, other: InfType) -> Literal[False]:
        ...

    @overload
    def __gt__(self, other: NegInfType) -> Literal[True]:
        ...

    def __gt__(self, other: int | InfType | NegInfType) -> bool:
        return other is not self

    @overload
    def __eq__(self, other: int) -> Literal[False]:
        ...

    @overload
    def __eq__(self, other: InfType) -> Literal[True]:
        ...

    @overload
    def __eq__(self, other: NegInfType) -> Literal[False]:
        ...

    def __eq__(self, other: int | InfType | NegInfType) -> bool:
        return other is self


@final
@total_ordering
class NegInfType(Singleton):
    """
    Negative infinity
    """

    def __repr__(self) -> str:
        return "NegInf"

    @overload
    def __lt__(self, other: int) -> Literal[True]:
        ...

    @overload
    def __lt__(self, other: InfType) -> Literal[True]:
        ...

    @overload
    def __lt__(self, other: NegInfType) -> Literal[False]:
        ...

    def __lt__(self, other: int | InfType | NegInfType) -> bool:
        return other is not self

    @overload
    def __eq__(self, other: int) -> Literal[False]:
        ...

    @overload
    def __eq__(self, other: InfType) -> Literal[False]:
        ...

    @overload
    def __eq__(self, other: NegInfType) -> Literal[True]:
        ...

    def __eq__(self, other: int | InfType | NegInfType) -> bool:
        return other is self


Inf = InfType()
NegInf = NegInfType()

__all__ = [
    "solve_quadratic",
    "product",
    "InfType",
    "Inf",
    "NegInfType",
    "NegInf",
]
