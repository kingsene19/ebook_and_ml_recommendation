from django.urls import path
from . import views

app_name = 'panier'

urlpatterns = [
    path('', views.panier_contenu, name='panier_contenu'),
    path('add/', views.panier_ajout, name='panier_ajout'),
    path('delete/', views.panier_supprimer, name='panier_supprimer'),
    path('update/', views.panier_maj, name='panier_maj'),
]
