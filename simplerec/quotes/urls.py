"""URLs for quotes views."""
from django.conf.urls import url

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', views.QuoteIndex.as_view()),
    url(r'^quotes/$', views.QuoteIndex.as_view(), name='quotes-index'),
    url(r'^quotes/(?P<pk>\d+)/$', views.QuoteDetail.as_view(),
        name='quotes-detail'),
]
