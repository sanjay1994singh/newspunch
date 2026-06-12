from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import NewsArticle
from category.models import Category


def robots_txt(request):
    content = """User-agent: *
    Allow: /
    Sitemap: https://newspunch24.com/sitemap.xml
    Sitemap: https://newspunch24.com/news-sitemap.xml
    """
    return HttpResponse(content, content_type="text/plain")


from django.shortcuts import render
from .models import NewsArticle, Category


def home(request):
    breaking_news = NewsArticle.objects.filter(
        status='published',
        is_breaking=True
    )[:5]

    latest_news = NewsArticle.objects.filter(
        status='published'
    )[:9]

    trending_news = NewsArticle.objects.filter(
        status='published'
    ).order_by('-views')[:6]

    categories = Category.objects.all()

    category_news = {}

    for cat in categories:
        category_news[cat.name] = NewsArticle.objects.filter(
            category=cat,
            status='published'
        )[:4]

    context = {

        "breaking_news": breaking_news,

        "latest_news": latest_news,

        "trending_news": trending_news,

        "categories": categories,

        "category_news": category_news,

    }

    return render(
        request,
        "home.html",
        context
    )


def news_detail(request, slug):
    news = get_object_or_404(NewsArticle, slug=slug, status='published')

    news.views += 1
    news.save()

    related_news = NewsArticle.objects.filter(category=news.category).exclude(id=news.id)[:5]

    return render(request, 'news_detail.html', {
        'news': news,
        'related_news': related_news
    })
