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
    'd': (1,),
    'e': (11, 12, 13),
    'f': (1, 20),
    'g': (30, 31),
    'h': (1, 3, 6),
    'i': (1, 3, 30),
    'j': (2,),
}


users = {
    k: {ad_id: 1 for ad_id in v} for k, v in users_src.items()
}


sim_ads = rec.similarity_data(users, rec.similarity_cosine)


def suggest(user_id):
    """Get suggested ad IDs for the given user."""
    return rec.recommend_items(sim_ads, users[user_id])
