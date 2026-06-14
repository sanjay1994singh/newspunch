from category.models import Category


def base_categories(request):
    return {
        "base_categories": Category.objects.all().order_by("name"),
    }
