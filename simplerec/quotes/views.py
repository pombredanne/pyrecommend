# coding: utf-8
"""Views for quotes."""
# pylint: disable=too-many-ancestors
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.views import generic

from . import models


class QuoteIndex(generic.ListView):
    """Show all quotes in the system."""
    queryset = models.Quote.objects.all()
