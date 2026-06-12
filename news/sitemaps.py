from django.contrib.sitemaps import Sitemap
from .models import NewsArticle


class NewsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.9

    def items(self):
        return NewsArticle.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
