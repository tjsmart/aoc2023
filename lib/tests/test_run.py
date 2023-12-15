import pytest

from ..run import _format_duration


@pytest.mark.parametrize(
    ("duration_ns", "expected"),
    [
        (1, "1.0 ns"),
        (12, "12.0 ns"),
        (123, "123.0 ns"),
        (1_234, "1.2 μs"),
        (12_345, "12.3 μs"),
        (123_456, "123.5 μs"),
        (1_234_567, "1.2 ms"),
        (12_345_678, "12.3 ms"),
        (123_456_789, "123.5 ms"),
        (1_234_567_890, "1.2  s"),
        (12_345_678_901, "12.3  s"),
        (60_000_000_000, "1.0 min"),
        (72_000_000_000, "1.2 min"),
    ],
)
def test_format_duration(duration_ns: int, expected: str):
    assert _format_duration(duration_ns) == expected
