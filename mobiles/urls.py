from django.urls import path
from django.http import HttpResponse

from .views import home, track_repair, sitemap, setup_admin


urlpatterns = [
    path(
        '',
        home,
        name='home'
    ),

    path(
        'track-repair/',
        track_repair,
        name='track_repair'
    ),

    path(
        'setup-admin/',
        setup_admin,
        name='setup_admin'
    ),

    path(
        'sitemap.xml',
        sitemap,
        name='sitemap'
    ),

    path(
        'robots.txt',
        lambda request: HttpResponse(
            """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /setup-admin/

Sitemap: https://ms-mobiles-4us8.onrender.com/sitemap.xml
""",
            content_type='text/plain'
        ),
        name='robots'
    ),
]