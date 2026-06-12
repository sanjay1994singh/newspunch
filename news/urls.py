from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<str:slug>/', views.news_detail, name='news_detail'),
    path("robots.txt", views.robots_txt),
]
