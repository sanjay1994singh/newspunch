from django.contrib.syndication.views import Feed
from .models import NewsArticle


class LatestNewsFeed(Feed):
    title = "News Punch 24 Latest News"
    link = "/"
    description = "Latest breaking news from News Punch 24"

    def items(self):
        return NewsArticle.objects.filter(status="published")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return item.get_absolute_url()
