from django import forms
from .models import Commande
import re


class CommandeForm(forms.ModelForm):

    choix = (('Wave', 'Wave'), ('OM', 'OM'),
             ('Livraison', 'Livraison'), ('Carte', 'Carte'),)
    nom_complet = forms.CharField(label='Nom Complet',
                                  min_length=4, max_length=50, help_text='Requis')
    email = forms.EmailField(max_length=100, help_text='Requis', error_messages={
                             'requis': 'Il faut renseigner un email valide'})
    adresse = forms.CharField(
        label='Adresse de facturation', help_text="Requis", max_length=100)
    methode = forms.ChoiceField(
        choices=choix, label='Choisissez votre methode de paiement', help_text='Requis')
    region = forms.CharField(label='Region', required=False)
    telephone = forms.CharField(label='Telephone', help_text='Requis')

    class Meta:
        model = Commande
        fields = ('nom_complet', 'email', 'adresse',
                  'methode', 'region', 'telephone')

    def clean_telephone(self):
        regex = "^[+][2][2][1]\s\d{2}\s\d{3}\s\d{2}\s\d{2}$"
        telephone = self.cleaned_data['telephone']
        if not re.fullmatch(regex, telephone):
            raise forms.ValidationError(
                "Le numéro de de télephone entré n'est pas au bon format")
        return telephone

    def clean_methode(self):
        methode = self.cleaned_data['methode']
        return methode

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom_complet'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Wolof Ndiaye'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'example@example.com', 'name': 'email', 'id': 'id_email'})
        self.fields['adresse'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Adresse de facturation'})
        self.fields['methode'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Votre methode de paiement'})
        self.fields['region'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Dakar'})
        self.fields['telephone'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '+221 xx xxx xx xx'})
