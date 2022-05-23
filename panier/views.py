from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from boutique.models import Produit
from .panier import Panier


def panier_contenu(request):
    panier = Panier(request)
    return render(request, 'panier/contenu.html', {'panier': panier})


def panier_ajout(request):
    panier = Panier(request)
    if request.POST.get('action') == 'post':
        produit_id = int(request.POST.get('produitid'))
        produit_qte = int(request.POST.get('produitqte'))
        produit = get_object_or_404(Produit, id=produit_id)
        panier.add(produit=produit, qte=produit_qte)
        panierqte = panier.__len__()
        response = JsonResponse({'qte': panierqte})
        return response


def panier_supprimer(request):
    panier = Panier(request)
    if request.POST.get('action') == 'post':
        produit_id = int(request.POST.get('produitid'))
        panier.delete(produit=produit_id)
        panierqte = panier.__len__()
        paniertotal = panier.total_prix()
        response = JsonResponse({'qte': panierqte, 'soustotal': paniertotal})
        return response


def panier_maj(request):
    panier = Panier(request)
    if request.POST.get('action') == 'post':
        produit_id = int(request.POST.get('produitid'))
        produit_qte = int(request.POST.get('produitqte'))
        panier.update(produit=produit_id, qte=produit_qte)

        panierqte = panier.__len__()
        paniertotal = panier.total_prix()
        response = JsonResponse({'qte': panierqte, 'soustotal': paniertotal})
        return response
