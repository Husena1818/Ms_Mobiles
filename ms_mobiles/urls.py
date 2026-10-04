from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap

from mobiles.sitemaps import StaticViewSitemap


def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://ms-mobiles-ogu4.onrender.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


sitemaps = {
    "static": StaticViewSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("mobiles.urls")),

    path("robots.txt", robots_txt, name="robots_txt"),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]