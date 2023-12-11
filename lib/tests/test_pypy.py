from .._pypy import rewrite_312


def test_rewrite_one_function():
    before = """\
def foo[T: int, **P](x: T, *args: P.args, **kwargs: P.kwargs) -> T:
    ...
"""
    expected_after = """\
import typing

T = typing.TypeVar("T", bound=int)
P = typing.ParamSpec("P")

def foo(x: T, *args: P.args, **kwargs: P.kwargs) -> T:
    ...
"""

    assert rewrite_312(before) == expected_after


def test_rewrite_one_type_alias():
    before = """\
type Foo = list[int]
"""
    expected_after = """\
import typing

Foo: typing.TypeAlias = list[int]
"""

    assert rewrite_312(before) == expected_after
