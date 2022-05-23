from django.contrib import admin
from .models import *


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Editeur)
class EditeurAdmin(admin.ModelAdmin):
    list_display = ["nom", "site", "email"]
    list_filter = ("nom",)


@admin.register(Contributeur)
class ContributeurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenoms', 'email']
    list_filter = ("nom",)
    search_fields = ('prenoms', 'nom')


@admin.register(ContributeurLivre)
class ContributeurLivreAdmin(admin.ModelAdmin):
    list_display = ["livre", "contributeur", "role"]
    list_filter = ("livre",)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ["titre", "date_publication", "editeur", "revues_positives", "revues_negatives"]
    list_filter = ("editeur", "contributeurs", 'date_publication')
    date_hierarchy = 'date_publication'
    search_fields = ('titre',)
    prepopulated_fields = {'slug': ('titre',)}


@admin.register(Revue)
class RevueAdmin(admin.ModelAdmin):
    list_display = ['user', 'produit', 'note']
    fieldsets = (('Linkage', {'fields': ('user', 'produit')}),
                 ('Review book', {'fields': ('contenu', 'note')}))
    list_filter = ('produit',)
