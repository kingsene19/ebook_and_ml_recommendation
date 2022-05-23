from django.urls import path

from . import views

app_name = 'commandes'

urlpatterns = [
    path('payer/', views.payer, name="payer"),
    path('confirmer/', views.confirmer, name="confirmer")
]
