from django.contrib import admin
from .models import Commande, ProduitCommande

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_commande', 'total_paye', 'methode']
    list_filter = ('date_commande', 'methode', 'user')

@admin.register(ProduitCommande)
class ProduitCommandeAdmin(admin.ModelAdmin):
    list_display = ['commande', 'produit', 'prix']
    