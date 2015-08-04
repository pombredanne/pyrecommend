# coding: utf-8
"""Recommendation stuff."""
from __future__ import division, unicode_literals
import math


class DictData(object):
    """A data access object for the recommendation algorithms.

    This reference implementation uses a Python dictionary as the underlying
    datastore. All suggestion methods are written with this object in mind, so
    by re-implenting the interface you can use the algorithms with e.g. the
    Django ORM or any other persistence/data source.

    """

    def __init__(self, data, default=None):
        self.data = data
        self.default = default

    @property
    def items(self):
        """All items eligible for reommendation in the system.

        Should not return any duplicate items.

        """
        return self.data.keys()

    @property
    def item_set(self):
        """Probably due to be deleted. No reason for this and `items`."""
        return set(self.items)

    def __getitem__(self, k):
        if self.default is not None:
            return self.data.get(k, self.default)
        else:

            # Data is organized in two layers:
            #   - a map of items to user's ratings
            #   - user ratings, themselves a map of users to numeric scores
            # When no default is present, assume it's because we're working on
            # the outer, item level. So if data[k] exists it will be a map of
            # user ratings, and for user ratings, we want a non-existent key
            # to have a score of 0.
            #
            # This is hacky and should probably be refactored.
            return DictData(self.data[k], default=0)

    def __repr__(self):
        return 'DictData({!r}, {!r})'.format(self.data, self.default)

    def __iter__(self):
        return iter(self.data)

    def values(self):
        """Get all... values? I don't even know why this is here..."""
        return self.data.values()


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


def mag_squared(vals):
    """Get the magnitude squared of the given iterable.

    In other words, get the sum of the squares of all values in vals.

    """
    return sum(v**2 for v in vals)


def mag(vals):
    """Get the magnitude of the given iterable."""
    return math.sqrt(mag_squared(vals))


def similarity_cosine(data_a, data_b):
    """Similarity between data_a and data_b using cosine."""

    all_keys = data_a.item_set | data_b.item_set

    if data_a and data_b:
        return (dot_product(data_a, data_b, all_keys)
                / (mag(data_a.values()) * mag(data_b.values())))
    else:
        return 0


def similarity_sorensen(data_a, data_b):
    """Get the Sørensen–Dice coefficient of data_a and data_b."""
    all_keys = data_a.item_set | data_b.item_set

    denom = (mag_squared(data_a.values()) + mag_squared(data_b.values()))

    if denom != 0:
        return (2 * dot_product(data_a, data_b, all_keys)) / denom
    else:
        return 0


def similar_sets(dataset, target, similarity=similarity_cosine):
    """Find other entries most similar to target.

    dataset is a dict of score mappings.

    target is the key in dataset of the thing that the other things should be
    similar to.

    """
    target_data = dataset[target]
    scores = ((similarity(target_data, dataset[k]), k)
              for k in dataset if k != target)
    return sorted(scores, reverse=True)


def similarity_data(dataset, result_storage=None, similarity=similarity_cosine):
    """Get a map of items to similar items using a ranking dataset."""
    result = result_storage if result_storage is not None else {}
    for item in dataset:
        similar_items = similar_sets(dataset, item, similarity=similarity)
        result[item] = similar_items
    return result


def recommend(similar_data, target):
    """Recommend things to `target` using prebuilt similarity data.

    Target should be a user profile (e.g. a scores map), not a user's name.

    """
    scores = {}
    for item, rating in target.items():
        for similarity, other_item in similar_data[item]:

            # target has rated this item so don't recommend it
            if target.get(other_item, 0) != 0:
                continue
            scores.setdefault(other_item, 0)
            scores[other_item] += similarity * rating

    rankings = ((score, item) for item, score in scores.items())
    return sorted(rankings, reverse=True)


def make_data(score_list):
    """Make numbered data dictionaries from a list of lists.

    >>> make_data([[5, 20], [30, 9]]) == {1: {1: 5, 2: 20}, 2: {1: 30, 2: 9}}
    True

    """
    data = {}
    for i, scores in enumerate(score_list):
        data[i+1] = {j+1: v for j, v in enumerate(scores) if v != 0}
    return data


def sim(*data, **kwargs):
    """Shorthand for calculating similarity data.

    All data is sent to `make_data`.

    >>> (sim([1, 2, 3], [4, 5, 6],
    ...      similarity=lambda a, b: len(a.values()) * len(b.values()))
    ...  == {(1, 2): 9})
    True

    """
    similarity = kwargs.pop('similarity', similarity_sorensen)
    if kwargs:
        raise ValueError('Unrecognized arguments: {}'.format(
            ', '.join(kwargs.keys())))
    ratings = make_data(data)
    sim_data = similarity_data(DictData(ratings), similarity=similarity)
    return make_pairs(sim_data)


def make_pairs(sim_data):
    """Take a dictionary of similarity data and make pairs of it instead.

    >>> (make_pairs({1: [(9, 2)], 2: [(9, 1)], 3: [(12, 5)]})
    ...  == {(1, 2): 9, (3, 5): 12})
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
