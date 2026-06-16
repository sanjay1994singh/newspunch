from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from category.models import Category

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


class CategorySitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.7

    def items(self):
        return Category.objects.all().order_by("name")

    def location(self, obj):
        return reverse("category_news", kwargs={"slug": obj.slug})


class StaticViewSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)
