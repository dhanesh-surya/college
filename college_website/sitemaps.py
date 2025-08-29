from django.contrib.sitemaps import Sitemap
from .models import Notice, Event, Program, Page


class NoticeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Notice.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Event.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProgramSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Program.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Page.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
