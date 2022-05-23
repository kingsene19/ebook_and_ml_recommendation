from django.shortcuts import render, redirect
from panier.panier import Panier
from .models import Commande, ProduitCommande
from .forms import CommandeForm
from django.contrib.auth.decorators import login_required


def confirmer(request):
    return render(request, "commandes/paiement_confirme.html")


def user_commande(request):
    user_id = request.user.id
    commandes = Commande.objects.filter(
        user_id=user_id).filter(paiement_effectue=True)
    return commandes

@login_required
def payer(request):
    if request.method == 'POST':
        commandeForm = CommandeForm(request.POST)
        if commandeForm.is_valid():
            dico = commandeForm.data.dict()
            del dico['csrfmiddlewaretoken']
            panier = Panier(request)
            user_id = request.user.id
            panier_total = panier.total_prix()
            commande = Commande.objects.create(
                user_id=user_id, total_paye=panier_total, **dico)
            commande_id = commande.pk
            for item in panier:
                ProduitCommande.objects.create(
                    commande_id=commande_id, produit=item['produit'], prix=item['prix'], quantite=item['qte'])
            panier.clear()
            return redirect('commandes:confirmer')
    else:
        commandeForm = CommandeForm()
    return render(request, "commandes/page_paiement.html", {'form': commandeForm})
