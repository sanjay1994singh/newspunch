from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import strip_tags
from django.utils.text import Truncator

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
    query = request.GET.get("q", "").strip()
    if query:
        articles = articles.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()

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
        "query": query,
        "seo_title": (
            f"Search results for {query} | NewsPunch"
            if query
            else "NewsPunch | Latest Breaking News"
        ),
        "seo_description": (
            f"Latest NewsPunch stories matching {query}."
            if query
            else "Latest breaking news, live updates, analysis, and fresh stories from NewsPunch."
        ),
        "canonical_url": request.build_absolute_uri(request.path),
    }
    return render(request, "home.html", context)


def news_detail(request, category_slug, slug):
    news = get_object_or_404(
        NewsArticle,
        slug=slug,
        status="published",
    )

    if news.category.slug != category_slug:
        return redirect(news.get_absolute_url(), permanent=True)

    NewsArticle.objects.filter(pk=news.pk).update(views=F("views") + 1)
    news.views += 1

    related_news = (
        NewsArticle.objects.filter(
            category=news.category,
            status="published",
        )
        .select_related("category", "author")
        .exclude(id=news.id)[:6]
    )

    latest_news = (
        NewsArticle.objects.filter(status="published")
        .select_related("category", "author")
        .exclude(id=news.id)[:6]
    )

    absolute_image_url = ""
    if news.image:
        absolute_image_url = request.build_absolute_uri(news.image.url)

    canonical_url = request.build_absolute_uri(news.get_absolute_url())
    description_source = news.meta_description or news.short_description or strip_tags(news.content)

    return render(
        request,
        "news_detail.html",
        {
            "news": news,
            "absolute_image_url": absolute_image_url,
            "related_news": related_news,
            "latest_news": latest_news,
            "categories": Category.objects.all().order_by("name"),
            "seo_title": news.meta_title or f"{news.title} | NewsPunch",
            "seo_description": Truncator(description_source).chars(155),
            "canonical_url": canonical_url,
        },
    )


def legacy_news_detail(request, slug):
    news = get_object_or_404(NewsArticle, slug=slug, status="published")
    return redirect(news.get_absolute_url(), permanent=True)


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
        "seo_title": f"{category.name} News | NewsPunch",
        "seo_description": (
            f"Latest {category.name} news, updates, explainers, and analysis from NewsPunch."
        ),
        "canonical_url": request.build_absolute_uri(request.path),
    }
    return render(request, "category_news.html", context)


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    news_sitemap_url = request.build_absolute_uri("/news-sitemap.xml")
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {sitemap_url}",
            f"Sitemap: {news_sitemap_url}",
            "",
        ]
    )
    return HttpResponse(content, content_type="text/plain")
