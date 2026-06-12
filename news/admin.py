from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

from .models import NewsArticle


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsArticle

        fields = "__all__"

        widgets = {

            "content": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5"
                },
                config_name="default"
            )

        }


@admin.register(NewsArticle)
class NewsAdmin(admin.ModelAdmin):
    form = NewsForm
