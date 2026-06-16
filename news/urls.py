from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("n/<int:pk>/", views.news_share_redirect, name="news_share_redirect"),
    path("category/<slug:slug>/", views.category_news, name="category_news"),
    path("news/<slug:category_slug>/<str:slug>/", views.news_detail, name="news_detail"),
    path("news/<str:slug>/", views.legacy_news_detail, name="legacy_news_detail"),
]
