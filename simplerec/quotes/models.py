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

    def __unicode__(self):
        return self.content


class FavoriteQuote(models.Model):
    """Track when a user 'favorites' a particular quote."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    quote = models.ForeignKey(Quote)

    def __unicode__(self):
        return '♥ {}: {}'.format(self.user, self.quote)

    class Meta:
        unique_together = ('user', 'quote')


class ViewedQuote(models.Model):
    """Track when a user views a quote."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    quote = models.ForeignKey(Quote)

    def __unicode__(self):
        return '✓ {}: {}"'.format(self.user, self.quote)

    class Meta:
        unique_together = ('user', 'quote')
