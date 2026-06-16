from django.contrib.sitemaps import Sitemap

from .models import NewsArticle


class GoogleNewsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return NewsArticle.objects.filter(status="published").order_by("-created_at")[:1000]

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at

    def publication_date(self, obj):
        return obj.created_at

    def news_publication(self):
        return {
            "name": "NewsPunch",
            "language": "en",
        }

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page=page, site=site, protocol=protocol)
        publication = self.news_publication()
        for url in urls:
            item = url["item"]
            url["news"] = {
                "publication": publication,
                "publication_date": item.created_at,
                "title": item.title,
            }
        return urls
