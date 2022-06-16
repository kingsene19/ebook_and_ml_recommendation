from django.urls import path
from . import views
from .api import rest_api

app_name = 'boutique'

urlpatterns = [
    path('all/', views.all_books, name='all_book'),
    path('achat/<slug:slug>', views.book_buy, name='book_buy'),
    path('boutique/<slug:category_slug>/',
         views.book_category, name='book_category'),
    path('modifier/<slug:slug>', views.mod_revue, name='modifier'),
    path('delete/', views.del_revue, name='supprimer'),
    path('api/produits/', rest_api, name="restAPI"),
]
