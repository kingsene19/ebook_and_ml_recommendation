from .models import Categorie


def categories(request):
    return {
        'categories': Categorie.objects.all()
    }
