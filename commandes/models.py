from django.conf import settings
from django.db import models
from boutique.models import Produit
from django.utils.translation import gettext_lazy as _


class Commande(models.Model):

    class PaimentMethodes(models.TextChoices):
        OM = "OrangeMoney", "OM"
        Wave = "Wave", "WAVE"
        Livrasion = "Livraison", "LIVRAISON"
        Carte = "Carte", "CARTE"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commande_user')
    nom_complet = models.CharField(_("Nom complet"), max_length=50)
    adresse = models.CharField(_("Adresse"), max_length=250)
    email = models.EmailField(_("Email"), max_length=100)
    region = models.CharField(_("Region"), max_length=100)
    telephone = models.CharField(_("Téléphone"), max_length=100)
    methode = models.CharField(verbose_name="Methode de paiement",
                               choices=PaimentMethodes.choices, max_length=20)
    date_commande = models.DateTimeField(
        _("Date de commande"), auto_now_add=True)
    paiement_effectue = models.BooleanField(
        _("Paiement effectué"), default=True)
    total_paye = models.IntegerField(_("Total à payer"))

    class Meta:
        ordering = ('-date_commande',)

    def __str__(self):
        return f"{self.user.user_name} {self.date_commande} {self.total_paye} {self.methode}"


class ProduitCommande(models.Model):
    commande = models.ForeignKey(Commande,
                                 related_name='produits',
                                 on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,
                                related_name='commande_elements',
                                on_delete=models.CASCADE)
    prix = models.IntegerField(_("Prix"))
    quantite = models.PositiveIntegerField(_("Quantité"), default=1)

    def __str__(self):
        return str(self.id)
