import re
from datetime import date

from accounts.models import User
from category.models import Category
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django_ckeditor_5.fields import CKEditor5Field


def hindi_slug(text):
    text = str(text).strip().lower()

    # Keep Devanagari, English letters, numbers, spaces, and hyphens.
    text = re.sub(r"[^\u0900-\u097Fa-zA-Z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    text = re.sub(r"-+", "-", text)

    return text.strip("-")


class NewsArticle(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news")

    short_description = models.TextField(null=True, blank=True)
    content = CKEditor5Field(
        "Content",
        config_name="default",
    )

    image = models.ImageField(upload_to="news/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_posts",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    is_breaking = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = hindi_slug(self.title)

            if not base_slug:
                base_slug = f"news-{NewsArticle.objects.count() + 1}"

            today = date.today().isoformat()
            slug = f"{today}-{base_slug}"
            counter = 1

            while NewsArticle.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{today}-{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if not self.meta_title:
            self.meta_title = Truncator(f"{self.title} | NewsPunch").chars(60)

        if not self.meta_description:
            source = self.short_description or strip_tags(self.content) or self.title
            self.meta_description = Truncator(source).chars(155)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "news_detail",
            kwargs={
                "category_slug": self.category.slug,
                "slug": self.slug,
            },
        )

    def __str__(self):
        return self.title
