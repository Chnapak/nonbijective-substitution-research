from experiment import make_mapping
import random

def test_make_mapping():
    mapping = make_mapping(16, [3, 2, 1], random.Random(42))

    assert len(mapping) == 16
    assert len(set(mapping.values())) == 10