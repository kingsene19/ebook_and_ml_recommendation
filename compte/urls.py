from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "compte"

urlpatterns = [

    # Statut utlisateur
    path('inscription/', views.compte_inscription, name='inscription'),
    path('login/', views.LoginView.as_view(), name='connexion'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/compte/login'), name='deconnexion'),

    # Profil utilisateur
    path('acceuil/', views.acceuil, name='acceuil'),
    path('profil/commandes/', views.liste_commandes, name='commandes'),

    path('profil/ajout_souhait/<int:id>',
         views.ajout_souhait, name="ajout_souhait"),
    path('profil/souhaits/', views.liste_souhaits, name="souhaits"),

    path('profil/modifier/', views.modifier, name='modifier'),
    path('profil/supprimer/', views.supprimer, name='supprimer'),
    path('profil/supprimer/confirmer', views.conf_supprimer, name='conf_sup'),
]
