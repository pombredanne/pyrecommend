"""Tests for the Quotes app."""
import pytest
from django.core import exceptions

from . import models


@pytest.mark.django_db
def test_quote_similarity_pk_order():
    """Pairs of quotes must be ordered by PK."""

    # Small/big in terms of their IDs.
    small_quote = models.Quote.objects.create(content='foo', pk=500)
    big_quote = models.Quote.objects.create(content='bar', pk=505)

    # Wrong order raises an exception.
    with pytest.raises(exceptions.ValidationError):
        models.QuoteSimilarity.objects.create(
            quote_1=big_quote, quote_2=small_quote, score=0.3)

    # Good order works fine.
    models.QuoteSimilarity.objects.create(
        quote_1=small_quote, quote_2=small_quote, score=0.3)
