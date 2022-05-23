from boutique.models import Produit
from django.conf import settings


class Panier():
    """
    Une classe Panier
    """

    def __init__(self, request):
        self.session = request.session
        panier = self.session.get(settings.PANIER_SESSION_ID)
        if settings.PANIER_SESSION_ID not in request.session:
            panier = self.session[settings.PANIER_SESSION_ID] = {}
        self.panier = panier

    def add(self, produit, qte):
        """
        Ajouter des produits au panier
        """
        produit_id = str(produit.id)

        if produit_id in self.panier:
            self.panier[produit_id]['qte'] = qte
        else:
            self.panier[produit_id] = {'prix': str(produit.prix), 'qte': qte}

        self.save()

    def __iter__(self):
        """
        Itérer sur les produits du panier
        """
        produit_ids = self.panier.keys()
        produits = Produit.objects.filter(id__in=produit_ids)
        panier = self.panier.copy()

        for produit in produits:
            panier[str(produit.id)]['produit'] = produit

        for item in panier.values():
            item['prix'] = int(item['prix'])
            item['total_prix'] = item['prix'] * item['qte']
            yield item

    def __len__(self):
        """
        Obtenir les données et les quantités du panier
        """
        return sum(item['qte'] for item in self.panier.values())

    def update(self, produit, qte):
        """
        Update values in session data
        """
        produit_id = str(produit)
        if produit_id in self.panier:
            self.panier[produit_id]['qte'] = qte
        self.save()

    def soustotal_prix(self):
        return sum(int(item['prix']) * item['qte'] for item in self.panier.values())

    def total_prix(self):

        soustotal = self.soustotal_prix()

        if soustotal == 0:
            shipping = 0
        else:
            shipping = 1500

        total = soustotal + (shipping)
        return total

    def delete(self, produit):
        """
        Delete item from session data
        """
        produit_id = str(produit)

        if produit_id in self.panier:
            del self.panier[produit_id]
            print(produit_id)
            self.save()

    def clear(self):
        del self.session[settings.PANIER_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True


"""
Code in this file has been inspried/reworked from other known works. Plese ensure that
the License below is included in any of your work that is directly copied from
this source file.


MIT License

Copyright (c) 2019 Packt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
