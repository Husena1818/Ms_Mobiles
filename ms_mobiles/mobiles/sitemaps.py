from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Mobile


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "mobiles",
            "repair",
            "track_repair",
            "register",
            "login",
            "cart",
        ]

    def location(self, item):
        return reverse(item)


class MobileSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Mobile.objects.all().order_by("id")

    def location(self, obj):
        return reverse("mobile_detail", args=[obj.id])