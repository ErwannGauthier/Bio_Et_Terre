# Create your models here.
from django.db import models

from accounts.models import Utilisateur


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    taux_tva = models.FloatField()
    image = models.URLField()


class Marque(models.Model):
    nom = models.CharField(max_length=100)


class Type(models.Model):
    nom = models.CharField(max_length=1000)
    unite_mesure = models.CharField(max_length=100)
    mesure = models.CharField(max_length=100)
    unite_mesure_petit = models.CharField(max_length=100)
    mesure_petit = models.CharField(max_length=100)


class Produit(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=1000)
    prix = models.FloatField()
    stock = models.IntegerField()
    description = models.CharField(max_length=10000)
    image = models.URLField(max_length=1000)
    achetable = models.BooleanField(default=True)
    quantite = models.FloatField()
    marque = models.ForeignKey(Marque, db_column="id_marque", on_delete=models.DO_NOTHING)
    categorie = models.ForeignKey(Categorie, db_column='id_categorie', on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, db_column='id_type', on_delete=models.DO_NOTHING)

    @property
    def calcTVA(self):
        return round((1 + self.categorie.taux_tva/100) * self.prix, 2)

    @property
    def getPoids(self):
        if self.type.id == 1:
            resultat = "Unité"
        else:
            if self.quantite < 1:
                if self.type.id == 2:
                        quantite = self.quantite * 1000
                elif self.type.id == 3:
                    quantite = self.quantite * 100
                mesure = self.type.mesure_petit
            else:
                quantite = self.quantite
                mesure = self.type.mesure

            if quantite - int(quantite) == 0:
                quantite = int(quantite)

            resultat = f"{quantite}{mesure}"

        return resultat

    @property
    def calcPrixPoids(self):
        if self.type.id == 1:
            resultat = f"{self.calcTVA}€/Unité"
        else:
            prix = round(self.calcTVA / self.quantite, 2)
            resultat = f"{prix}€/{self.type.mesure}"

        return resultat

class Commande(models.Model):
    id = models.AutoField(primary_key=True)
    utilisateur = models.ForeignKey(Utilisateur, db_column='id_utilisateur', on_delete=models.DO_NOTHING, blank=True, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    est_complete = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        produits = Commande_Produit.objects.filter(commande=self).order_by('produit__id')
        return round(sum([produit.calcPrixTotal for produit in produits]), 2)

    @property
    def get_cart_items(self):
        produits = Commande_Produit.objects.filter(commande=self).order_by('produit__id')
        return sum([produit.quantite for produit in produits])


class Commande_Produit(models.Model):
    id = models.AutoField(primary_key=True)
    commande = models.ForeignKey(Commande, db_column='id_commande', on_delete=models.DO_NOTHING, blank=True, null=True)
    produit = models.ForeignKey(Produit, db_column='id_produit', on_delete=models.DO_NOTHING, blank=True, null=True)
    quantite = models.IntegerField()

    @property
    def calcPrixTotal(self):
        return round(self.quantite * self.produit.prix, 2)
