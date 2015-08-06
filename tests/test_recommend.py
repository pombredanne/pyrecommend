"""Tests for the pyrecommend module."""
from pyrecommend import rec


def make_data(*values):
    """Make a 1-indexed DictData from a list."""
    return rec.DictData({i+1: v for i, v in enumerate(values)},
                        default=0)


def test_cosine_similarity():
    """Cosine similarity calculations are correct."""
    data_a = make_data(2, 1, 0, 2, 0, 1, 1, 1)
    data_b = make_data(2, 1, 1, 1, 1, 0, 1, 1)

    similarity = rec.similarity_cosine(data_a, data_b)

    assert round(similarity, 3) == 0.822


def test_dot_product():
    """Dot product calculations are correct."""
    data_a = make_data(5, 0, 3, 2)
    data_b = make_data(1, 3, 4, 9)

    product = rec.dot_product(data_a, data_b)

    assert 35 == product
