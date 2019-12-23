from itertools import chain, repeat, islice
from pipe import take, chain_with

import pytest

lst1 = [1, 2, 3]


def pythonic_always_6_elements(seq, padded_length):
    return seq + [None] * (padded_length - len(seq))


def iter_always_6_elements(seq, padded_length):
    return islice(chain(seq, repeat(None)), padded_length)


def pipe_always_6_elements(seq, padded_length):
    return (seq | chain_with(repeat(None))
            | take(padded_length))

@pytest.mark.parametrize("seq, func, padded_length", [
    (lst1, pythonic_always_6_elements, 6),
    (lst1, iter_always_6_elements, 6),
    (lst1, pipe_always_6_elements, 6),
#    (range(4), pythonic_always_6_elements, 11),
    (range(4), iter_always_6_elements, 11),
    (range(4), pipe_always_6_elements, 11),
])
def test_iter(seq, func, padded_length):
    assert len(list(func(seq, padded_length))) == padded_length
