from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.category_news, name="category_news"),
    re_path(r"^news/(?P<slug>.+?)/?$", views.news_detail, name="news_detail"),
]
