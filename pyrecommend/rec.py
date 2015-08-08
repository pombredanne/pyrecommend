# coding: utf-8
"""A library for item-to-item collaborative filtering.

The primary function of interest is `calculate_similarity`, which will
calculate similarity scores for pairs of items from a given dataset.

There are also a few similarity calculations to choose from in the `similarity`
module.

This library is in an extremely early state.

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import itertools


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


def similar_sets(dataset, target, similarity):
    """Find other entries most similar to target.

    dataset is a dict of score mappings.

    target is the key in dataset of the thing that the other things should be
    similar to.

    """
    target_data = dataset[target]
    scores = ((similarity(target_data, dataset[k]), k)
              for k in dataset if k != target)
    return sorted(scores, reverse=True)


def get_dict_values(item_a, item_b, data):
    """Get index-aligned lists for all values in item_a and item_b.

    >>> # This is a slightly strange example since the order of the keys is
    >>> # arbitrary. The order doesn't matter, however the pairing does, which
    >>> # is why a set() of the zip() of the two lists should show the function
    >>> # is correct.
    >>>
    >>> one_items, two_items = get_dict_values('one', 'two',
    ...     {'one': {'a': 9, 'b': 50},
    ...      'two': {'a': 7, 'b': 35},
    ...      'three': {'a': 9999}})
    >>> set(zip(one_items, two_items)) == {(9, 7), (50, 35)}
    True

    """
    data_a = data[item_a]
    data_b = data[item_b]
    all_keys = set(data_a.keys()) | set(data_b.keys())
    a_values = [data_a.get(k, 0) for k in all_keys]
    b_values = [data_b.get(k, 0) for k in all_keys]
    return a_values, b_values


def calculate_similarity(dataset, similarity, result_storage=None,
                         get_values=get_dict_values):
    """Get a map of items to similar items using a ranking dataset.

    result_storage:
        an object implementing __getitem__ where all results are stored.

    get_values:
        a callable taking two keys and the dataset, which needs to return two
        lists, essentially 'vectorizing' the data from the dataset for the two
        items. See get_dict_values() for an example.

    """
    result = result_storage if result_storage is not None else {}
    for item_a, item_b in itertools.combinations(dataset, 2):
        a_values, b_values = get_values(item_a, item_b, dataset)
        sim_score = similarity(a_values, b_values)
        result[(item_a, item_b)] = sim_score
    return result


# TODO: this is untested; in my use case a function like this doesn't appear to
# be needed. Might change in the future, however.
def __recommend(similar_data, target):  # pragma: no cover
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
