import math
from collections.abc import Iterable
from typing import overload


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


__all__ = [
    "solve_quadratic",
    "product",
]
