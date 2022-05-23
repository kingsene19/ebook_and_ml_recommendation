from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserBase


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Adresse mail', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    prenoms = forms.CharField(label='Entrer votre nom complet')
    user_name = forms.CharField(
        label='Entrer votre username', min_length=4, max_length=50, help_text='Requis')
    email = forms.EmailField(max_length=100, help_text='Requis', error_messages={
                             'requis': 'Il faut renseigner un email'})
    password = forms.CharField(
        label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Répéter mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'email', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Répéter mot de passe'})
        self.fields['prenoms'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Wolof Ndiaye'})


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Email du compte (Non modifiable)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Nom d\'utilisateur', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname'}))

    prenoms = forms.CharField(
        label='Prenoms', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Prenom(s)', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'prenoms',)

    def cleaned_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
