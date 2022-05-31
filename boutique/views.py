from msilib.schema import Error
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from yaml import load
from .utils import average_rating, load_models, load_data
from .models import *
from .forms import RevueForm
from django.contrib.auth.decorators import login_required


model_sa, model_br = load_models()
pivot_df, livres = load_data()

# Create your views here.


def all_books(request):
    produits = Produit.objects.all()
    return render(request, 'boutique/all_books.html', {'produits': produits})


def book_category(request, category_slug=None):
    categorie = get_object_or_404(Categorie, slug=category_slug)
    produits = Produit.objects.filter(categorie=categorie)
    return render(request, 'boutique/book_category.html', {'categorie': categorie, 'produits': produits})


def book_buy(request, slug):
    produit = get_object_or_404(Produit, slug=slug, en_stock=True)
    revues = produit.revue_set.all()
    note = average_rating([revue.note for revue in revues])
    cat = get_object_or_404(Categorie, slug="litterature")
    if request.method == "POST":
        user_id = request.user.id
        revueForm = RevueForm(request.POST)
        if revueForm.is_valid():
            note = revueForm.cleaned_data.get('note')
            avis = revueForm.cleaned_data.get('contenu')
            Revue.objects.create(
                user_id=user_id, produit_id=produit.id, note=note, contenu=avis)
            prediction = model_sa.predict([avis])[0]
            if prediction == 2:
                produit.revues_positives += 1
            else:
                produit.revues_negatives += 1
            produit.save()
    else:
        revueForm = RevueForm()
    if produit in Produit.objects.filter(categorie=cat):
        try:
            revue = produit.revue_set.filter(user_id=request.user.id)[0]
        except Exception:
            revue = []
            return render(request, 'boutique/book_buy.html', {'produit': produit, 'produit': produit, "note": note, "revues": revues, 'form': revueForm})
        else:
            if model_sa.predict([revue.contenu])[0] == 2:
                preds = []
                query_index = pivot_df.index.get_loc(produit.titre)
                distances, indices = model_br.kneighbors(
                    pivot_df.iloc[query_index, :].values.reshape(1, -1), n_neighbors=6)
                for i in range(len(distances.flatten())-1, 1, -1):
                    preds.append([pivot_df.index[indices.flatten()[i]], livres.loc[livres['bookTitle']
                                                                                   == pivot_df.index[indices.flatten()[i]]]['imageUrlS'].values[0]])
                com = f'{request.user.prenoms} ravi de voire que ce livre vous ait plus. Votre satisfaction est notre bonheur 😊.'
                produit.save()
                return render(request, 'boutique/book_buy.html', {'produit': produit, "note": note, "revues": revues, 'com': com, 'preds': preds, 'form': revueForm})
            else:
                message = "Désolé que ce livre ne vous ai pas plu, parcourez notre bibliothèque"
                com = f'{request.user.prenoms} désolé que ce livre ne soit pas à la hauteur de vos attentes. Nous tenterons d\'améliorer votre expérience 😔'
                return render(request, 'boutique/book_buy.html', {'produit': produit, "note": note, "revues": revues, 'message': message, 'com': com, 'form': revueForm})
    return render(request, 'boutique/book_buy.html', {'produit': produit, "note": note, "revues": revues, "form": revueForm})


@login_required
def del_revue(request):
    if request.POST.get('action') == 'post':
        revue_id = int(request.POST.get('revueid'))
        revue = Revue.objects.filter(id=revue_id)[0]
        livre = revue.produit
        if model_sa.predict([revue.contenu])[0] == 2:
            livre.revues_positives -= 1
            livre.save()
        else:
            livre.revues_negatives -= 1
            livre.save()
        Revue.objects.filter(id=revue_id).delete()
        response = JsonResponse({'Success': 'data'})
        return response


@login_required
def mod_revue(request, slug):
    if request.method == "POST":
        livre = get_object_or_404(Produit, slug=slug)
        user_id = request.user.id
        revue = livre.revue_set.filter(user_id=user_id)
        revueForm = RevueForm(request.POST)
        if revueForm.is_valid():
            print("valide")
            note = revueForm.cleaned_data.get('note')
            avis = revueForm.cleaned_data.get('contenu')
            revue.update(note=note)
            revue.update(contenu=avis)
        return redirect(livre.get_relative_url())
    else:
        revueForm = RevueForm()
        livre = get_object_or_404(Produit, slug=slug)
    return render(request, 'boutique/add_revue.html', {'form': revueForm, 'produit': livre})


def home(request):
    produits = Produit.objects.all()[:6]
    return render(request, 'home.html', {'produits': produits})


def contact(request):
    return render(request, 'contact.html')
