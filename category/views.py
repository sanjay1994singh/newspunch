from django.shortcuts import render, get_object_or_404
from .models import Category
from news.models import NewsArticle


def category_detail(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug
    )

    news = NewsArticle.objects.filter(
        category=category,
        status='published'
    )

    context = {

        "category": category,

        "news": news,

    }

    return render(
        request,
        "category.html",
        context
    )
