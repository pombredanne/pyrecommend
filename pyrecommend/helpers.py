# coding: utf-8
"""Utilities that make experimenting in a Python shell easier."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import rec


def make_data(score_list):
    """Make numbered data dictionaries from a list of lists.

    This is for easily simulating scores for items by ID, rated by users where
    the users are identified by ID as well.

    This is to help when playing in the shell.

    >>> make_data([[5, 20], [30, 9]]) == {1: {1: 5, 2: 20}, 2: {1: 30, 2: 9}}
    True

    """
    data = {i+1: {j+1: v for j, v in enumerate(scores) if v != 0}
            for i, scores in enumerate(score_list)}
    return data


def sim(*data, **kwargs):
    """Shorthand for quickly calculating similarity for small datasets.

    data: one or more lists of ratings. Each list represents an 'item' and each
          number in that list is a rating by a user; users are assumed to be
          the same between all lists.

    similarity: a keyword-only argument; the similarity function to use.

    Useful for playing in the shell.

    >>> from .similarity import dot_product
    >>> sim([1, 0, 5], [1, 1, 1], similarity=dot_product)
    {(1, 2): 6}

    """

    # Python 2 doesn't support keyword-only arguments.
    similarity = kwargs.pop('similarity')
    if kwargs:
        raise ValueError('Unused kwargs: {}'.format(kwargs.keys()))

    ratings = make_data(data)
    sim_data = rec.calculate_similarity(
        rec.DictData(ratings), similarity=similarity)
    return make_pairs(sim_data)


def make_pairs(sim_data):
    """Convert a dict of item-indexed data to pair-indexed.

    >>> data = {1: [(0.333, 2)], 2: [(0.333, 1)], 3: [(0.84, 5)]}
    >>> make_pairs(data) == {(1, 2): 0.333, (3, 5): 0.84}
    True

    """
    result = {}
    for item_a, sim_items in sim_data.items():
        for sim_score, item_b in sim_items:
            if item_a < item_b:
                pair = item_a, item_b
            else:
                pair = item_b, item_a
            result[pair] = sim_score
    return result
