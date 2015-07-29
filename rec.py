"""Recommendation stuff."""
from __future__ import division, unicode_literals
import collections
import math


def similarity_cosine(data_a, data_b):
    """Similarity between data_a and data_b using cosine."""

    common_keys = data_a.viewkeys() | data_b.viewkeys()

    def dot_product():  # pylint: disable=missing-docstring
        result = 0
        for k in common_keys:
            result += data_a.get(k, 0) * data_b.get(k, 0)
        return result

    def mag(data):
        """Get the magnitude of the values of a dictionary."""
        return math.sqrt(sum(v**2 for v in data.values()))

    if data_a and data_b:
        return dot_product() / (mag(data_a) * mag(data_b))
    else:
        return 0


def similar_sets(dataset, target, similarity=similarity_cosine):
    """Find other entries most similar to target.

    dataset is a dict of score mappings.

    target is the key in dataset of the thing that the other things should be
    similar to.

    """
    data_points = dataset.viewkeys() - {target}
    target_data = dataset[target]
    scores = ((similarity(target_data, dataset[k]), k)
              for k in data_points)
    return sorted(scores, reverse=True)


def similarity_data(dataset, similarity=similarity_cosine):
    """Get a map of items to similar items using a ranking dataset."""
    result = {}
    for item in dataset:
        similar_items = similar_sets(dataset, item, similarity=similarity)
        result[item] = similar_items
    return result


def recommend(similar_data, target):
    """Recommend things to `target` using prebuilt similarity data.

    Target should be a user profile (e.g. a scores map), not a user's name.

    """
    scores = collections.defaultdict(lambda: 0)

    for item, rating in target.items():
        for similarity, other_item in similar_data[item]:

            # target has rated this item so don't recommend it
            if target.get(other_item, 0) != 0:
                continue
            scores[other_item] += similarity * rating

    rankings = ((score, item) for item, score in scores.items())
    return sorted(rankings, reverse=True)
