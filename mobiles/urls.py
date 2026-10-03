from django.urls import path
from django.views.generic import TemplateView

from .views import home, track_repair, sitemap


urlpatterns = [
    path('', home, name='home'),

    path(
        'track-repair/',
        track_repair,
        name='track_repair'
    ),

    path(
        'sitemap.xml',
        sitemap,
        name='sitemap'
    ),

    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
        ),
        name='robots'
    ),
]