from django.db import models
from django.utils.text import slugify
from category.models import Category
from django.urls import reverse
from accounts.models import User
import re
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField


def hindi_slug(text):
    text = str(text).strip().lower()

    # keep Hindi + English + numbers + spaces
    text = re.sub(
        r'[^ऀ-ॿa-zA-Z0-9\s-]',
        '',
        text
    )

    # replace spaces with hyphen
    text = re.sub(r'[\s]+', '-', text)

    # remove duplicate hyphens
    text = re.sub(r'-+', '-', text)

    return text.strip('-')


class NewsArticle(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')

    short_description = models.TextField(null=True, blank=True)
    content = RichTextUploadingField()

    image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_posts')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    is_breaking = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = hindi_slug(self.title)

            if not base_slug:
                base_slug = f'news-{NewsArticle.objects.count() + 1}'

            today = date.today().isoformat()

            slug = f"{today}-{base_slug}"
            counter = 1

            while NewsArticle.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{today}-{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # SEO TITLE (OPTIMIZED)
        if not self.meta_title:
            self.meta_title = f"{self.title} | {date.today().isoformat()} | News Punch 24"

        # SEO DESCRIPTION (OPTIMIZED)
        if not self.meta_description:
            self.meta_description = f"{self.short_description[:140]}... {date.today().isoformat()} पर अपडेट | News Punch 24"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
