from itertools import chain, repeat, islice
from pipe import take, chain_with

import pytest

lst1 = [1, 2, 3]


def pythonic_always_6_elements(lst):
    return lst + [None] * (6 - len(lst))


def iter_always_6_elements(lst):
    return islice(chain(lst, repeat(None)), 6)


def pipe_always_6_elements(lst):
    return (lst | chain_with(repeat(None))
                | take(6))

@pytest.mark.parametrize("lst, func", [
    (lst1, pythonic_always_6_elements),
    (lst1, iter_always_6_elements),
    (lst1, pipe_always_6_elements),
#    (range(4), pythonic_always_6_elements),
    (range(4), iter_always_6_elements),
    (range(4), pipe_always_6_elements),
])
def test_iter(lst, func):
    assert len(list(func(lst))) == 6
