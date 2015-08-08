# coding: utf8
"""Tests for the rec module."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pyrecommend


def test_similarity():
    """Similarity calculations work as advertised."""
    data = {'X': {'a': 1, 'b': 5},
            'Y': {'a': 3, 'b': 2, 'c': 10},
            'Z': {'b': 4, 'c': 1}}

    def add_all(data_a, data_b):
        """Add up all the numbers in both lists."""
        return sum(data_a) + sum(data_b)

    results = pyrecommend.calculate_similarity(data, add_all)

    # For comparing to expected results, turn pairs to sets.
    results = {frozenset(k): v for k, v in results.items()}

    assert results == {
        frozenset('XY'): 21,
        frozenset('XZ'): 11,
        frozenset('YZ'): 20,
    }
