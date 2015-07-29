"""/admin/ config for the quotes app."""
from django.contrib import admin

from . import models


@admin.register(models.Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Admin class for quotes."""
