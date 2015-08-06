# coding: utf-8
"""Tests for the pyrecommend module."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from pyrecommend import rec, similarity


def make_data(*values):
    """Make a 1-indexed DictData from a list."""
    return rec.DictData({i+1: v for i, v in enumerate(values)},
                        default=0)


def test_cosine_similarity():
    """Cosine similarity calculations are correct."""
    data_a = make_data(2, 1, 0, 2, 0, 1, 1, 1)
    data_b = make_data(2, 1, 1, 1, 1, 0, 1, 1)

    sim_score = similarity.cosine(data_a, data_b)

    assert round(sim_score, 3) == 0.822


def test_dot_product():
    """Dot product calculations are correct."""
    data_a = make_data(5, 0, 3, 2)
    data_b = make_data(1, 3, 4, 9)

    sim_score = similarity.dot_product(data_a, data_b)

    assert sim_score == 35


def test_sorensen():
    """Sorensen coefficients are correct."""
    data_a = make_data(4, 0, 1, 3)
    data_b = make_data(3, 1, 0, 5)

    sim_score = similarity.sorensen(data_a, data_b)

    assert round(sim_score, 3) == 0.885
