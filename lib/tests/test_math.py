import pytest

from ..math import Inf
from ..math import NegInf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_inf_lt(value):
    assert value < Inf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_inf_eq(value):
    assert value != Inf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_inf_min(value):
    assert min(Inf, value) == value


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_inf_max(value):
    assert max(Inf, value) == Inf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_neginf_gt(value):
    assert value > NegInf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_neginf_eq(value):
    assert value != NegInf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_neginf_min(value):
    assert min(NegInf, value) == NegInf


@pytest.mark.parametrize("value", [-1, 0, 1, 100000])
def test_neginf_max(value):
    assert max(NegInf, value) == value
