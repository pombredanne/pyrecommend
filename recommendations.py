"""Recommendation stuff."""
from __future__ import division, unicode_literals
import collections
import math


def similarity_distance(data_a, data_b):
    """Get similarity between two datasets by Euclidean distance."""

    # Find all items they both have
    shared_items = data_a.viewkeys() & data_b.viewkeys()

    # Find Euclidean distance
    def dist_term(item):
        """Get an additive component of the distance formula."""
        return pow(data_a[item] - data_b[item], 2)
    sum_of_squares = sum(dist_term(k) for k in shared_items)
    return 1/(1 + sum_of_squares)


def similarity_pearson(data_a, data_b):
    """Get similarity between two datasets by Pearson coefficient."""

    def values(dict_, keys):
        """Get multiple values from dict_."""
        return (dict_[k] for k in keys)

    def pearson_numerator(a_vals, b_vals):
        """Get the numerator of the Pearson coefficient."""
        sum_products = sum(a * b for a, b in zip(a_vals, b_vals))
        sum_a = sum(a_vals)
        sum_b = sum(b_vals)
        numerator = sum_products - (sum_a * sum_b / len(shared_items))
        return numerator

    def pearson_denominator(a_vals, b_vals):
        """Get the denominator of the Pearson coefficient."""

        def fact(values):
            """Get the pearson factor of the given set of values."""
            sum_squared = pow(sum(values), 2)
            sum_squares = sum(pow(n, 2) for n in values)
            return sum_squares - sum_squared / len(values)

        return math.sqrt(fact(a_vals) * fact(b_vals))

    shared_items = data_a.viewkeys() & data_b.viewkeys()
    if not shared_items:
        return 0

    a_scores = list(values(data_a, shared_items))
    b_scores = list(values(data_b, shared_items))
    denominator = pearson_denominator(a_scores, b_scores)
    if denominator == 0:
        return 0
    numerator = pearson_numerator(a_scores, b_scores)
    return numerator / denominator


def similar_sets(dataset, target, similarity=similarity_pearson):
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


def similarity_data(dataset, similarity=similarity_distance):
    """Get a map of items to similar items using a ranking dataset."""
    result = {}
    item_rankings = invert_data(dataset)
    for item in item_rankings:
        similar_items = similar_sets(item_rankings, item,
                                     similarity=similarity)
        result[item] = similar_items
    return result


def recommend(dataset, target, similarity=similarity_pearson):
    """Recommend things to `target`.

    dataset is a dict of score mappings. E.g. a dict mapping users to a map of
    their ratings of various items.

    `target` is a single user from that dict.

    """
    totals = collections.defaultdict(lambda: 0)
    similar_sums = collections.defaultdict(lambda: 0)
    target_ratings = dataset[target]
    for person, ratings in dataset.items():
        if person == target:
            continue

        sim = similarity(target_ratings, ratings)

        # Ignore completely dissimilar users
        if sim <= 0:
            continue

        for item, score in ratings.items():
            if target_ratings.get(item, 0) != 0:
                continue
            totals[item] += score * sim
            similar_sums[item] += sim

    rankings = ((total / similar_sums[k], k) for k, total in totals.items())
    return sorted(rankings, reverse=True)


def invert_data(dataset):
    """Take a map of one thing to rankings of another thing, and invert it.

    E.g. take a map of user's rankings of products and turn it into a map of
    products to their rankings by each user.

    """
    flipped = {}
    for item, ratings in dataset.items():
        for rater, rating in ratings.items():
            flipped.setdefault(rater, {})[item] = rating
    return flipped


def recommend_items(similar_data, target):
    """Recommend things to `target` using prebuilt similarity data.

    Target should be a user profile (e.g. a scores map), not a user's name.

    """
    scores = collections.defaultdict(lambda: 0)
    similarity_totals = collections.defaultdict(lambda: 0)

    for item, rating in target.items():
        for similarity, other_item in similar_data[item]:

            # target has rated this item so don't recommend it
            if other_item in target:
                continue
            scores[other_item] += similarity * rating
            similarity_totals[other_item] += similarity
    rankings = ((score / similarity_totals[item], item)
                for item, score in scores.items())
    return sorted(rankings, reverse=True)
