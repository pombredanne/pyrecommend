"""Parser for MovieLens data."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import codecs
import os.path


def fopen(*args, **kwargs):
    """Open a file with UTF-8 by default."""
    kwargs.setdefault('encoding', 'iso-8859-1')
    return codecs.open(*args, **kwargs)


def load_movielens_data(path):
    """Read data from MovieLens into a dict of user rankings."""
    movie_filename = os.path.join(path, 'u.item')
    ratings_filename = os.path.join(path, 'u.data')

    movies = {}
    with fopen(movie_filename) as movie_file:
        for line in movie_file:
            movie_id, title = line.split('|')[:2]
            movies[movie_id] = title

    users_ratings = {}
    with fopen(ratings_filename) as ratings_file:
        for line in ratings_file:

            # _ is timestamp, unused field
            user, movie_id, rating, _ = line.split()
            movie = movies[movie_id]
            users_ratings.setdefault(user, {})[movie] = int(rating)
    return users_ratings
