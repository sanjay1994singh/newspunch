from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from news.sitemaps import NewsSitemap
from news.google_news_sitemap import GoogleNewsSitemap
from news.feeds import LatestNewsFeed

sitemaps = {
    "news": NewsSitemap,
    "news-google": GoogleNewsSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('category/', include('category.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns += [
    path("rss.xml", LatestNewsFeed()),
]

urlpatterns += [
    path("news-sitemap.xml", sitemap, {"sitemaps": {"news": GoogleNewsSitemap}}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
