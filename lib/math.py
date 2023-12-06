import math

def solve_quadratic(a: float, b: float, c: float) -> tuple[float, float]:
    return (
        (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a),
        (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a),
    )


__all__ = [
    "solve_quadratic",
]
