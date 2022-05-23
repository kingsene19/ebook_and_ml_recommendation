from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from boutique.models import Produit
from .forms import RegistrationForm, UserEditForm, UserLoginForm
from .models import UserBase
from commandes.models import Commande
from commandes.views import user_commande
from django.contrib.auth import views as views_auth
from django.utils.translation import gettext_lazy as _


# Create your views here.
class LoginView(views_auth.LoginView):
    form_class = UserLoginForm
    redirect_authenticated_user = True
    template_name = 'compte/inscription/connexion.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '../../admin'
        return '../../compte/acceuil'


def compte_inscription(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.prenoms = registerForm.cleaned_data['prenoms']
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()
            return redirect('compte:connexion')
    else:
        registerForm = RegistrationForm()
    return render(request, 'compte/inscription/inscrire.html', {'form': registerForm})


@login_required
def acceuil(request):
    commandes = user_commande(request)
    return render(request, 'compte/user/acceuil.html', {'commandes': commandes})


@login_required
def liste_commandes(request):
    user_id = request.user.id
    commandes = Commande.objects.filter(
        user_id=user_id).filter(paiement_effectue=True)
    return render(request, "compte/user/liste_commandes.html", {"commandes": commandes})


@login_required
def ajout_souhait(request, id):
    produit = get_object_or_404(Produit, id=id)
    if produit.in_user_souhait.filter(id=request.user.id).exists():
        produit.in_user_souhait.remove(request.user)
        messages.success(request, produit.titre +
                         _(" a été retiré de votre liste de souhaits"))
    else:
        produit.in_user_souhait.add(request.user)
        messages.success(request, _("Ajout de ") +
                         produit.titre + _(" à votre liste de souhaits"))
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def liste_souhaits(request):
    produits = Produit.objects.filter(in_user_souhait=request.user)
    return render(request, "compte/user/liste_de_souhaits.html", {"produits": produits})


@login_required
def modifier(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'compte/user/modifier.html', {'user_form': user_form})


@login_required
def supprimer(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('compte:conf_sup')


def conf_supprimer(request):
    return render(request, 'compte/user/confirmer_suppression.html')
