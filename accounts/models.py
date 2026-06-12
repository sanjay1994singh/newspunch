from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('author', 'Author'),
        ('reporter', 'Reporter'),
        ('subscriber', 'Subscriber'),
    )

    # IMPORTANT NEWS PROFILE FIELDS
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, blank=True, null=True)

    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='author')

    is_verified = models.BooleanField(default=False)

    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_editor = models.BooleanField(default=False)
    is_reporter = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"
