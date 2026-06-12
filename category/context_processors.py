from .models import Category


def common_data(request):
    return {

        "menu_categories": Category.objects.all()

    }
