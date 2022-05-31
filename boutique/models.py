from wsgiref.simple_server import demo_app
from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class Editeur(models.Model):
    """
        Une maison d'édition
    """
    nom = models.CharField(max_length=50, help_text="Nom de l'éditeur")
    site = models.URLField(help_text="Site de l'éditeur")
    email = models.EmailField(help_text="Email de l'éditeur")

    def __str__(self):
        return self.nom


class Contributeur(models.Model):
    """ Un contributeur d'un livre, i.e author,co-author,editor"""
    prenoms = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField()

    def initialled_name(self):
        abr = []
        for elts in self.prenoms.split(" "):
            abr.append(elts[0])
        return '{},{}'.format(self.nom, [abrs for abrs in abr].pop())

    def __str__(self):
        return self.initialled_name()


class Categorie(models.Model):
    nom = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('boutique:book_category', args=[self.slug])

    def __str__(self):
        return self.nom


class Produit(models.Model):
    """ Un livre publié """
    titre = models.CharField(max_length=255)
    categorie = models.ForeignKey(
        Categorie, related_name='product', on_delete=models.CASCADE)
    editeur = models.ForeignKey(Editeur, on_delete=models.CASCADE)
    contributeurs = models.ManyToManyField(
        'Contributeur', through="ContributeurLivre", related_name='contributeur')
    description = models.TextField(blank=True)
    date_publication = models.DateField()
    image = models.ImageField(upload_to="images/", null=True)
    slug = models.SlugField(max_length=255)
    prix = models.IntegerField()
    en_stock = models.BooleanField(default=True)
    in_user_souhait = models.ManyToManyField(
        User, related_name='user_souhait', blank=True)
    revues_positives = models.IntegerField(default=0)
    revues_negatives = models.IntegerField(default=0)

    class Meta:
        ordering = ('-date_publication',)

    def get_absolute_url(self):
        return reverse('boutique:book_buy', args=[self.slug])

    def get_mod_url(self):
        return reverse('boutique:modifier', args=[self.slug])

    def __str__(self):
        return self.titre


class ContributeurLivre(models.Model):
    """Établit la relation entre le livre et la table des contributeurs car ils sont dans une relation plusieurs à plusieurs.
    Le rôle est un champ intermédiaire que nous utilisons pour stocker la relation entre eux. La classe ContributionRole est utilisée pour définir un ensemble de choix en créant une sous-classe de TextChoices.
    Fait référence à un ensemble de choix définis dans les modèles, utiles lors de la création de Django Forms.
    """
    class ContributionRole(models.TextChoices):
        AUTEUR = "AUTEUR", "Auteur"
        CO_AUTEUR = "CO_AUTEUR", "Co-Auteur"

    livre = models.ForeignKey(
        Produit, on_delete=models.CASCADE, related_name='livre')
    contributeur = models.ForeignKey(Contributeur, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="Role de ce contributeur",
                            choices=ContributionRole.choices, max_length=20)


class Revue(models.Model):
    contenu = models.TextField()
    note = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="createur")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
