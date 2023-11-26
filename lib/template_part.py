def solution(s: str) -> int:
    ...


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            ("", 0),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
