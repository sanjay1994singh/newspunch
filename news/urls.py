from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<str:slug>/", views.category_news, name="category_news"),
    path("news/<str:slug>/", views.news_detail, name="news_detail"),
]
