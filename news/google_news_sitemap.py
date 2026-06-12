from django.contrib.sitemaps import Sitemap
from .models import NewsArticle
from datetime import datetime


class GoogleNewsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return NewsArticle.objects.filter(status="published")

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at

    def publication_date(self, obj):
        return obj.created_at

    def news_publication(self):
        return {
            "name": "News Punch 24",
            "language": "en",
        }
