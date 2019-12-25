from collections import Mapping
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from types import FunctionType
from typing import Any

KEEP = lambda f1, f2: f1 if f1 is not None else f2
COMBINE_STR = lambda f1, f2: "".join([(f1 or ""), (f2 or "")])
OVERWRITE = lambda f1, f2: f2 if f2 is not None else f1


@dataclass
class Key:
    """
    A "Key" is meant to represent a column type and maps to values. It can be used as a map key and - most
    importantly - has a strategy for how to combine its values.
    """
    name: str
    merge_strategy: FunctionType = OVERWRITE

    def __hash__(self):
        """ Currently assumes names are unique """
        return self.name.__hash__()

    def __eq__(self, other):
        """ Currently assumes names are unique """
        return self.name == other.name


A = Key("A")
B = Key("B")
C = Key("C", merge_strategy=COMBINE_STR)
D = Key("D")
E = Key("E", merge_strategy=KEEP)
F = Key("F")

results = [
    {A: "a", B: "b1", C: "c1"},
    {B: "b2", C: "c2", E: 1, F: 2},
    {C: "c3", D: 3, E: 4}
]

################################################################
# Solution 1 - merge each "level" of results, one pair at a time
################################################################


def merge_values(key, value1, value2):
    strategy = key.merge_strategy if isinstance(key, Key) else OVERWRITE
    return strategy(value1, value2)


def merge_levels(m1: Mapping, m2: Mapping) -> Mapping:
    keys = set(chain(m1.keys(), m2.keys()))
    return {k: merge_values(k, m1.get(k), m2.get(k)) if k in m2 else m1.get(k)
            for k in keys}


def merge_level_by_level(results):
    return reduce(merge_levels, results, {})


def test_merging_level_by_level():
    result = reduce(merge_levels, results, {})

    assert result[C] == "c1c2c3"
    assert result[E] == 1


#########################################################################
# Solution 2 - merge all "levels" of values, one key/Field at a time
#########################################################################

def combine_values(accumulated, entry):
    field, values = entry
    value = reduce(field.merge_strategy, values)
    return {**accumulated,
            field: value}


def test_merging_field_by_field():
    all_the_fields = set(chain(*map(dict.keys, results)))
    values_in_level_order = {f: [r.get(f, None) for r in results] for f in all_the_fields}

    combined_values = reduce(combine_values, values_in_level_order.items(), {})

    assert combined_values[A] == "a"
    assert combined_values[F] == 2
    assert combined_values[C] == "c1c2c3"
    assert combined_values[E] == 1


