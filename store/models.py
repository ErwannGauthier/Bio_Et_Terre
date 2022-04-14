# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from accounts.models import User


class Categorie(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    tauxtva = models.FloatField(db_column='tauxTVA')  # Field name made lowercase.
    image = models.URLField()

    class Meta:
        managed = False
        db_table = 'categorie'


class Commande(models.Model):
    id_panier = models.ForeignKey('Panier', models.DO_NOTHING, db_column='id_panier', primary_key=True)
    id_utilisateur = models.OneToOneField(User, models.DO_NOTHING, db_column='id_utilisateur')
    date_validation = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'commande'
        unique_together = (('id_panier', 'id_utilisateur'),)

    @property
    def get_cart_total(self):
        produits = EstComposeDe.objects.filter(id_panier=self.id_panier).order_by('id_produit')
        return round(sum([produit.calcPrixTotal for produit in produits]), 2)

    @property
    def get_cart_items(self):
        produits = EstComposeDe.objects.filter(id_panier=self.id_panier).order_by('id_produit')
        return sum([produit.quantite for produit in produits])


class EstComposeDe(models.Model):
    id_produit = models.OneToOneField('Produit', models.DO_NOTHING, db_column='id_produit', primary_key=True)
    id_panier = models.ForeignKey('Panier', models.DO_NOTHING, db_column='id_panier')
    quantite = models.IntegerField()

    @property
    def calcPrixTotal(self):
        return round(self.quantite * self.id_produit.prix, 2)

    class Meta:
        managed = False
        db_table = 'est_compose_de'
        unique_together = (('id_produit', 'id_panier'),)


class Liquide(models.Model):
    id_prod = models.OneToOneField('Produit', models.DO_NOTHING, db_column='id_prod', primary_key=True)
    litre = models.FloatField()

    class Meta:
        managed = False
        db_table = 'liquide'


class Marque(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'marque'


class Panier(models.Model):
    id = models.IntegerField(primary_key=True)
    valide = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'panier'


class Produit(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=1000)
    prix = models.FloatField()
    qtt_stock = models.IntegerField()
    descript = models.CharField(max_length=10000)
    image = models.URLField(max_length=1000)
    marque = models.ForeignKey(Marque, models.DO_NOTHING, db_column='id_marque')
    categorie = models.ForeignKey(Categorie, models.DO_NOTHING, db_column='id_categorie')
    achetable = models.BooleanField(default=True)

    def calcTVA(self):
        return round((1 + self.categorie.tauxtva/100) * self.prix, 2)

    def calcPrixType(self):
        try:
            type = Solide.objects.get(pk=self.id)
            prix = self.calcTVA()/type.kg
            diminutif = "Kilo"
            poids = type.kg
            if poids < 1:
                poids = poids * 1000
                mesure = "g"
            else:
                mesure = diminutif
        except Exception as e:
            #print(e)
            try:
                type = Liquide.objects.get(pk=self.id)
                prix = self.calcTVA() / type.litre
                diminutif = "Litre"
                poids = type.litre
                if poids < 1:
                    poids = poids * 100
                    mesure = "cl"
                else:
                    mesure = diminutif
            except Exception as e:
                #print(e)
                try:
                    type = Unite.objects.get(pk=self.id)
                    diminutif = "Unité"
                    prix = self.calcTVA()
                    poids = -1
                    mesure = diminutif
                except Exception as e:
                    print(e)

        return [round(prix, 2), diminutif, poids, mesure]

    def getQttType(self):
        try:
            type = Solide.objects.get(pk=self.id)
            qtt = type.kg
        except Exception as e:
            try:
                type = Liquide.objects.get(pk=self.id)
                qtt = type.litre
            except Exception as e:
                try:
                    type = Unite.objects.get(pk=self.id)
                    qtt = -1
                except Exception as e:
                    print(e)
        return qtt

    class Meta:
        managed = False
        db_table = 'produit'


class Solide(models.Model):
    id_prod = models.OneToOneField(Produit, models.DO_NOTHING, db_column='id_prod', primary_key=True)
    kg = models.FloatField()

    class Meta:
        managed = False
        db_table = 'solide'


class Unite(models.Model):
    id_prod = models.OneToOneField(Produit, models.DO_NOTHING, db_column='id_prod', primary_key=True)

    class Meta:
        managed = False
        db_table = 'unite'


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    pass_field = models.CharField(db_column='pass', max_length=100)  # Field renamed because it was a Python reserved word.
    mail = models.EmailField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'utilisateur'
