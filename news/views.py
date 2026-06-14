from urllib.parse import quote, unquote, unquote_plus

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from category.models import Category

from .models import NewsArticle


def _published_articles():
    return (
        NewsArticle.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at")
    )


def _slug_candidates(slug):
    values = []
    current = str(slug or "").split("?", 1)[0].split("#", 1)[0].strip().strip("/")
    current = current.replace("\\", "/").strip("/")

    for _ in range(3):
        for value in {current, unquote(current), unquote_plus(current)}:
            value = value.strip().strip("/")
            value = value.replace("\u2013", "-").replace("\u2014", "-")
            value = value.replace("\u00a0", "-")
            if value and value not in values:
                values.append(value)

        decoded = unquote(current)
        if decoded == current:
            break
        current = decoded.strip().strip("/")

    return values


def _get_shared_article(slug):
    candidates = _slug_candidates(slug)
    query = Q()

    for candidate in candidates:
        query |= Q(slug=candidate)
        query |= Q(slug__iexact=candidate)

    article = _published_articles().filter(query).first() if query else None
    if article:
        return article

    raise Http404("No published NewsArticle matches this shared URL.")


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
    article = _get_shared_article(slug)

    NewsArticle.objects.filter(pk=article.pk).update(views=F("views") + 1)
    article.views += 1

    related_articles = (
        _published_articles()
        .filter(category=article.category)
        .exclude(pk=article.pk)[:4]
    )
    article_url = request.build_absolute_uri(article.get_absolute_url())
    article_display_url = unquote(article_url)
    article_image_url = request.build_absolute_uri(article.image.url) if article.image else ""
    share_text = f"{article.title}\n{article_display_url}"

    context = {
        "article": article,
        "article_url": article_url,
        "article_display_url": article_display_url,
        "article_image_url": article_image_url,
        "whatsapp_share_url": f"https://api.whatsapp.com/send?text={quote(share_text)}",
        "facebook_share_url": f"https://www.facebook.com/sharer/sharer.php?u={quote(article_url, safe='')}",
        "twitter_share_url": f"https://twitter.com/intent/tweet?url={quote(article_url, safe='')}&text={quote(article.title)}",
        "telegram_share_url": f"https://t.me/share/url?url={quote(article_url, safe='')}&text={quote(article.title)}",
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
