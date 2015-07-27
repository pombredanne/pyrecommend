"""An environment script to make shell usage easy.

Use::

    python --interactive recommend_shell.py

"""
# pylint: disable=invalid-name
import copy
from pprint import pprint  # pylint: disable=unused-import

import movielens
import rec
from critics import critics

movies = rec.invert_data(critics)
movielens = movielens.load_movielens_data('ml-100k')


def pad_zero(dicts):
    """Ensure all dicts have all same keys, inserting zeroes when needed."""
    all_keys = reduce(lambda a, b: a | b, (d.viewkeys() for d in dicts))
    for dict_ in dicts:
        for k in all_keys:
            dict_.setdefault(k, 0)


# A "test sample" of users. Map of usernames to ad IDs they've applied to
users_src = {
    'a': (1, 2, 3),
    'b': (1, 3, 5),
    'c': (10, 11, 12),
}

users = {
    k: {ad_id: 1 for ad_id in v} for k, v in users_src.items()
}

users_zero = copy.deepcopy(users)
pad_zero(users_zero.values())
sim_ads = rec.similarity_data(users_zero, rec.similarity_pearson)
