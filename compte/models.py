from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **champs):

        champs.setdefault('is_staff', True)
        champs.setdefault('is_superuser', True)
        champs.setdefault('is_active', True)

        if champs.get('is_staff') is not True:
            raise ValueError(
                'Superuser doit avoir is_staff=True.')
        if champs.get('is_superuser') is not True:
            raise ValueError(
                'Superuser doit avoir is_superuser=True.')

        return self.create_user(email, user_name, password, **champs)

    def create_user(self, email, user_name, password, **champs):

        if not email:
            raise ValueError(_('Il faut fournir une email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          password=password, **champs)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('Adresse email'), unique=True)
    user_name = models.CharField(
        _('Nom utilisateur'), max_length=150, unique=True)
    prenoms = models.CharField(
        _('Nom complet'), max_length=150, blank=True)
    a_propos = models.TextField(_('A propos'), max_length=500, blank=True)
    # Détails de la livraison
    pays = CountryField(_("Pays de résidence"))
    telephone = models.CharField(_("Téléphone"), max_length=15, blank=True)
    addresse = models.CharField(_("Adresse"), max_length=150, blank=True)
    ville = models.CharField(_("Ville"), max_length=150, blank=True)
    # Statut utilisateur
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cree = models.DateTimeField(_("Créé le"), auto_now_add=True)
    modifie = models.DateTimeField(_("Modifié le"), auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = _("Compte")
        verbose_name_plural = _("Comptes")

    def __str__(self):
        return self.user_name
