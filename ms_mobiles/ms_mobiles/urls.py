from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap

from mobiles.sitemaps import StaticViewSitemap, MobileSitemap


sitemaps = {
    "static": StaticViewSitemap,
    "mobiles": MobileSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("mobiles.urls")),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]