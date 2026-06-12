from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/', views.category_detail, name='category_detail'),
]
