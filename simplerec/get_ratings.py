"""Interface between suggestion algorithm and Django quote app."""
import django.contrib.auth.models  # pylint: disable=unused-import
from django.contrib import auth
from django.db.models import Q
from pyrecommend import rec

import quotes.models


def ratings_for(obj):
    """Get all ratings for a quote or a user."""
    ratings = {}

    if hasattr(obj, 'username'):
        # If we're getting the ratings for a user, we're looking at all the
        # different quotes they rated.
        def key(quote_obj):
            """Associate each score with a quote."""
            return quote_obj.quote

    else:
        # If we're getting ratings fora quote, we're looking at all the
        # different users that rated it.
        def key(quote_obj):
            """Associate each score with a user."""
            return quote_obj.user

    for vquote in obj.viewedquote_set.all():
        ratings[key(vquote)] = 1
    for fquote in obj.favoritequote_set.all():
        ratings[key(fquote)] = 5
    return ratings


class QuoteData(object):  # pylint: disable=too-few-public-methods
    """Provide access to quote data to recommendation algorithm."""

    def __init__(self, quote):
        self.quote = quote

    @property
    def items(self):
        """Get all quotes that are somehow related to this quote."""
        quote = self.quote

        # Get all users who viewed or favorited this quote
        relevant_users = auth.models.User.objects.filter(
            Q(favoritequote__quote=quote) | Q(viewedquote__quote=quote)
        ).distinct()

        # Get all quotes that said users have viewed or favorited (will
        # include 'quote')
        relevant_quotes = quotes.models.Quote.objects.filter(
            Q(favoritequote__user__in=relevant_users) |
            Q(viewedquote__user__in=relevant_users)
        ).distinct()
        return relevant_quotes.prefetch_related(
            'viewedquote_set', 'favoritequote_set')

    def __getitem__(self, quote):
        """Get all user ratings for this quote."""
        return rec.DictData(ratings_for(quote), 0)

    def __iter__(self):
        return iter(self.items)


class ResultStorage(object):  # pylint: disable=too-few-public-methods
    """Write scores into the database."""

    @classmethod
    def __setitem__(cls, quote, similarity_scores):
        for score, other_quote in similarity_scores:
            quotes.models.QuoteSimilarity.store(quote, other_quote, score)


def turn_to_pks(sim_data):
    """Change a similarity data dictionary to use PKs instead of models.

    This makes it slightly easier to read data when futzing with the shell.

    """
    return {key.pk: [(score, quote.pk) for score, quote in val]
            for key, val in sim_data.items()}
