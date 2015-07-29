# coding: utf-8
"""Models for quote stuff."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings
from django.core import urlresolvers
from django.db import models


class Quote(models.Model):
    """Some text that someone finds memorable."""

    content = models.CharField(max_length=400, unique=True)

    def get_absolute_url(self):
        """Get a URL to this quote's detail page."""
        return urlresolvers.reverse('quotes-detail', kwargs={'pk': self.pk})

    def mark_viewed_by(self, user):
        """Record that the given Django user viewed this quote."""
        ViewedQuote.objects.get_or_create(user=user, quote=self)

    def is_favorited_by(self, user):
        """Check if user has favorited this quote."""
        return FavoriteQuote.objects.filter(user=user, quote=self).exists()

    def mark_favorite_for(self, user):
        """Mark this as a favorite quote for user."""
        FavoriteQuote.objects.get_or_create(user=user, quote=self)

    def unmark_favorite_for(self, user):
        """Remove favorite mark for the given user."""
        FavoriteQuote.objects.filter(user=user, quote=self).delete()

    def __unicode__(self):
        return self.content


class FavoriteQuote(models.Model):
    """Track when a user 'favorites' a particular quote."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    quote = models.ForeignKey(Quote)

    def __unicode__(self):
        star_symbol = '\u2605'
        return '{} {}: {}'.format(star_symbol, self.user, self.quote)

    class Meta:
        unique_together = ('user', 'quote')


class ViewedQuote(models.Model):
    """Track when a user views a quote."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    quote = models.ForeignKey(Quote)

    def __unicode__(self):
        checkmark = '\u2713'
        return '{} {}: {}'.format(checkmark, self.user, self.quote)

    class Meta:
        unique_together = ('user', 'quote')
