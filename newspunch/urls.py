from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from news import views as news_views
from news.sitemaps import CategorySitemap, NewsSitemap, StaticViewSitemap
from news.google_news_sitemap import GoogleNewsSitemap
from news.feeds import LatestNewsFeed

sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "news": NewsSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('category/', include('category.urls')),
    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls")
    ),

]

urlpatterns += [
    path("rss.xml", LatestNewsFeed(), name="rss_feed"),
    path("robots.txt", news_views.robots_txt, name="robots_txt"),
]

urlpatterns += [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path(
        "news-sitemap.xml",
        sitemap,
        {
            "sitemaps": {"news": GoogleNewsSitemap},
            "template_name": "sitemap_news.xml",
        },
        name="google_news_sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
