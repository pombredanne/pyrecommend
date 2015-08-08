# coding: utf-8
"""Tests for the pyrecommend module."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from pyrecommend import similarity


def test_cosine_similarity():
    """Cosine similarity calculations are correct."""
    data_a = [2, 1, 0, 2, 0, 1, 1, 1]
    data_b = [2, 1, 1, 1, 1, 0, 1, 1]

    sim_score = similarity.cosine(data_a, data_b)

    assert round(sim_score, 3) == 0.822


def test_cosine_empty():
    """Cosine between two empty lists is zero."""
    assert similarity.cosine([], []) == 0


def test_dot_product():
    """Dot product calculations are correct."""
    data_a = [5, 0, 3, 2]
    data_b = [1, 3, 4, 9]

    sim_score = similarity.dot_product(data_a, data_b)

    assert sim_score == 35


def test_sorensen():
    """Sorensen coefficients are correct."""
    data_a = [4, 0, 1, 3]
    data_b = [3, 1, 0, 5]

    sim_score = similarity.sorensen(data_a, data_b)

    assert round(sim_score, 3) == 0.885


def test_sorensen_empty():
    """Sorensen coefficient of two empty lists is 0."""
    assert similarity.sorensen([], []) == 0
