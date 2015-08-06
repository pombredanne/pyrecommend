# coding: utf-8
"""Similarity functions for recommendation calculations."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import vec_util


def dot_product(data_a, data_b, all_keys=None):
    """Get the dot product between two dictionaries.

    Uses each key given in common_keys. I.e. each common_key is a dimension,
    and the dict value for that key is the scalar value for that dimension.

    """
    if all_keys is None:
        all_keys = data_a.item_set | data_b.item_set
    result = 0
    for k in all_keys:
        result += data_a[k] * data_b[k]
    return result


def cosine(data_a, data_b):
    """Similarity between data_a and data_b using cosine."""

    all_keys = data_a.item_set | data_b.item_set

    denom = vec_util.mag(data_a.values()) * vec_util.mag(data_b.values())
    if denom:
        return dot_product(data_a, data_b, all_keys) / denom
    else:
        return 0


def sorensen(data_a, data_b):
    """Get the Sørensen–Dice coefficient of data_a and data_b."""
    all_keys = data_a.item_set | data_b.item_set

    denom = (vec_util.mag_squared(data_a.values()) +
             vec_util.mag_squared(data_b.values()))

    if denom != 0:
        return (2 * dot_product(data_a, data_b, all_keys)) / denom
    else:
        return 0
