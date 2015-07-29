"""URLs for quotes views."""
from django.conf.urls import url

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', views.QuoteIndex.as_view()),
]
