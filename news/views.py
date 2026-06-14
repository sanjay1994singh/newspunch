from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, render

from category.models import Category

from .models import NewsArticle


def _published_articles():
    return (
        NewsArticle.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at")
    )


def home(request):
    articles = _published_articles()
    categories = Category.objects.all().order_by("name")

    featured_article = articles.filter(is_breaking=True).first() or articles.first()
    latest_articles = articles.exclude(pk=getattr(featured_article, "pk", None))[:6]
    briefing_articles = articles.exclude(pk=getattr(featured_article, "pk", None))[:4]

    category_sections = []
    for category in categories:
        category_articles = articles.filter(category=category)[:3]
        if category_articles:
            category_sections.append(
                {
                    "category": category,
                    "articles": list(category_articles),
                }
            )

    context = {
        "featured_article": featured_article,
        "latest_articles": latest_articles,
        "briefing_articles": briefing_articles,
        "categories": categories,
        "category_sections": category_sections,
        "breaking_articles": articles.filter(is_breaking=True)[:5],
        "popular_articles": articles.order_by("-views", "-created_at")[:5],
    }
    return render(request, "home.html", context)


def news_detail(request, slug):
    article = get_object_or_404(
        _published_articles(),
        slug=slug,
    )

    NewsArticle.objects.filter(pk=article.pk).update(views=F("views") + 1)
    article.views += 1

    related_articles = (
        _published_articles()
        .filter(category=article.category)
        .exclude(pk=article.pk)[:4]
    )
    article_url = request.build_absolute_uri(article.get_absolute_url())
    article_image_url = request.build_absolute_uri(article.image.url) if article.image else ""

    context = {
        "article": article,
        "article_url": article_url,
        "article_image_url": article_image_url,
        "related_articles": related_articles,
        "categories": Category.objects.all().order_by("name"),
    }
    return render(request, "news_detail.html", context)


def category_news(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = _published_articles().filter(category=category)

    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
        "articles": page_obj.object_list,
        "categories": Category.objects.all().order_by("name"),
        "popular_articles": _published_articles().order_by("-views", "-created_at")[:5],
    }
    return render(request, "category_news.html", context)
