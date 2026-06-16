from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.category_news, name="category_news"),
    path("news/<slug:category_slug>/<str:slug>/", views.news_detail, name="news_detail"),
    path("news/<str:slug>/", views.legacy_news_detail, name="legacy_news_detail"),
]
