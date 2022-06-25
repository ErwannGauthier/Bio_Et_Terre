from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.urls import reverse

from store.models import Marque, Produit, Categorie, Type

User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    template = loader.get_template("administration/admin_index.html")

    context = {}

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    template = loader.get_template("administration/admin_categories.html")

    categories = Categorie.objects.all()
    context = {
        'categories': categories
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def categories_ajouter(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        taux_tva = request.POST.get("taux_tva")
        image = request.POST.get("image")
        categorie = Categorie.objects.get_or_create(nom=nom, taux_tva=taux_tva, image=image)
        return redirect('administration:categories')

    template = loader.get_template("administration/admin_categories_ajouter.html")
    context = {}
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def categories_modifier(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    if request.method == "POST":
        nom = request.POST.get("nom")
        taux_tva = float(request.POST.get("taux_tva"))
        image = request.POST.get("image")
        if categorie.nom != nom or categorie.taux_tva != taux_tva or categorie.image != image:
            categorie.nom = nom
            categorie.taux_tva = taux_tva
            categorie.image = image
            categorie.save()
            return redirect('administration:categories')
        else:
            messages.error(request, "Vous n'avez pas modifié la catégorie.")

    template = loader.get_template("administration/admin_categories_modif.html")
    context = {
        'categorie': categorie
    }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def categories_supprimer(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    if request.method == "POST":
        categorie.delete()
        return redirect('administration:categories')

    template = loader.get_template("administration/admin_categories_delete.html")
    produits = Produit.objects.filter(categorie=categorie)
    context = {
        'categorie': categorie,
        'produits': produits
    }
    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def clients(request):
    template = loader.get_template("administration/admin_clients.html")

    clients = User.objects.filter(is_superuser=0).order_by("id")
    context = {
        'clients': clients
    }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def marques(request):
    template = loader.get_template("administration/admin_marques.html")

    marques = Marque.objects.all()
    context = {
        'marques': marques
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def marques_ajouter(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        marque = Marque.objects.get_or_create(nom=nom)
        return redirect('administration:marques')

    template = loader.get_template("administration/admin_marques_ajouter.html")
    context = {}
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def marques_modifier(request, id):
    marque = get_object_or_404(Marque, id=id)

    if request.method == "POST":
        nom = request.POST.get("nom")
        if marque.nom != nom:
            marque.nom = nom
            marque.save()
            return redirect('administration:marques')
        else:
            messages.error(request, "Vous n'avez pas modifié la marque.")

    template = loader.get_template("administration/admin_marques_modif.html")
    context = {
        'marque': marque
    }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def marques_supprimer(request, id):
    marque = get_object_or_404(Marque, id=id)

    if request.method == "POST":
        marque.delete()
        return redirect('administration:marques')

    template = loader.get_template("administration/admin_marques_delete.html")
    produits = Produit.objects.filter(marque=marque)
    context = {
        'marque': marque,
        'produits': produits
    }
    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def produits(request):
    template = loader.get_template("administration/admin_produits.html")
    produits = Produit.objects.filter(achetable=1).order_by("categorie__id")
    context = {
        'produits': produits
    }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def produits_detail(request, id):
    template = loader.get_template("administration/admin_produits_detail.html")
    produit = Produit.objects.get(pk=id)
    if produit.type.id != 1 and produit.quantite < 1:
        if produit.type.id == 2:
            quantite = produit.quantite * 1000
        elif produit.type.id == 3:
            quantite = produit.quantite * 100
        mesure = produit.type.mesure_petit
        prix = round(produit.calcTVA / produit.quantite, 2)
        context = {
            'produit': produit,
            'quantite':quantite,
            'mesure': mesure,
            'prix': prix
        }
    else:
        context = {
            'produit': produit,
            'prix': produit.calcTVA
        }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def produits_ajouter(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        prix = float(request.POST.get("prix"))
        stock = int(request.POST.get("stock"))
        description = request.POST.get("description")
        image = request.POST.get("image")

        marque_id = int(request.POST.get("marque"))
        if marque_id == -1:
            marque_nom = request.POST.get("marque_nom")
            marque = Marque.objects.get_or_create(nom=marque_nom)[0]
        else:
            marque = Marque.objects.get(pk=marque_id)

        categorie_id = int(request.POST.get("categorie"))
        if categorie_id == -1:
            categorie_nom = request.POST.get("categorie_nom")
            categorie_tva = float(request.POST.get("categorie_tva"))
            categorie_image = request.POST.get("categorie_image")
            categorie = Categorie.objects.get_or_create(nom=categorie_nom, taux_tva=categorie_tva, image=categorie_image)[0]
        else:
            categorie = Categorie.objects.get(pk=categorie_id)

        type_id = int(request.POST.get("type"))
        if type_id == 2:
            quantite = float(request.POST.get("solide"))
        elif type_id == 3:
            quantite = float(request.POST.get("liquide"))
        else:
            quantite = 0
        type = Type.objects.get(pk=type_id)

        id = Produit.objects.filter(categorie=categorie.id).aggregate(Max('id'))['id__max']
        if id:
            id = str(int(id[:id.find('_')]) + 1) + "_0"
        else:
            id = str(categorie.id * 10000 + 1) + "_0"

        produit = Produit.objects.get_or_create(id=id, nom=nom, prix=prix, stock=stock, description=description, image=image, categorie=categorie, marque=marque, type=type, quantite=quantite)
        return redirect('administration:produits')

    template = loader.get_template("administration/admin_produits_ajouter.html")
    marque = Marque.objects.all().order_by('nom')
    categorie = Categorie.objects.all().order_by('nom')
    type = Type.objects.all().order_by('nom')
    context = {
        'marques': marque,
        'categories': categorie,
        'types': type
    }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def produits_modifier(request, id):
    produit = get_object_or_404(Produit, id=id)

    if produit.achetable == 0:
        return redirect('administration:produits')

    if request.method == "POST":
        nom = request.POST.get("nom")
        prix = float(request.POST.get("prix"))
        stock = int(request.POST.get("stock"))
        description = request.POST.get("description")
        image = request.POST.get("image")
        marque_id = int(request.POST.get("marque"))
        categorie_id = int(request.POST.get("categorie"))
        type_id = int(request.POST.get("type"))
        if type_id == 2:
            quantite = float(request.POST.get("solide"))
        elif type_id == 3:
            quantite = float(request.POST.get("liquide"))
        else:
            quantite = 0

        if produit.nom != nom or produit.prix != prix or produit.stock != stock or produit.description != description or produit.image != image or produit.marque.id != marque_id or produit.categorie.id != categorie_id or produit.type.id != type_id or produit.quantite != quantite:
            if marque_id == -1:
                marque_nom = request.POST.get("marque_nom")
                marque = Marque.objects.get_or_create(nom=marque_nom)
            else:
                marque = Marque.objects.get(pk=marque_id)

            if categorie_id == -1:
                categorie_nom = request.POST.get("categorie_nom")
                categorie_tva = float(request.POST.get("categorie_tva"))
                categorie_image = request.POST.get("categorie_image")
                categorie = Categorie.objects.get_or_create(nom=categorie_nom, taux_tva=categorie_tva,
                                                            image=categorie_image)
            else:
                categorie = Categorie.objects.get(pk=categorie_id)

            type = Type.objects.get(pk=type_id)
            new_id = id[:(id.find('_') + 1)] + str(int(id[(id.find('_') + 1):]) + 1)

            produit.achetable = 0
            produit.save()

            new_produit = Produit.objects.get_or_create(id=new_id, nom=nom, prix=prix, stock=stock, description=description, image=image, categorie=categorie, marque=marque, type=type, quantite=quantite)
            return HttpResponseRedirect(reverse('administration:produits_detail', args=[new_produit[0].id]))
        else:
            messages.error(request, "Vous n'avez pas modifié le produit.")

    template = loader.get_template("administration/admin_produits_modif.html")
    marques = Marque.objects.all().order_by('nom')
    categories = Categorie.objects.all().order_by('nom')
    types = Type.objects.all().order_by('nom')
    context = {
        'produit': produit,
        'marques': marques,
        'categories': categories,
        'types': types
    }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def produits_modifier_stock(request, id):
    produit = get_object_or_404(Produit, id=id)

    if produit.achetable == 0:
        return redirect('administration:produits')

    if request.method == "POST":
        stock = int(request.POST.get("stock"))
        produit.stock = stock
        produit.save()
        return HttpResponseRedirect(reverse('administration:produits_detail', args=[id]))

    template = loader.get_template("administration/admin_produits_modif_stock.html")
    context = {
        'produit': produit
    }
    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def produits_supprimer(request, id):
    produit = get_object_or_404(Produit, id=id)

    if request.method == "POST":
        produit.achetable = 0
        produit.save()
        return HttpResponseRedirect(reverse('administration:produits_detail', args=[produit.id]))

    template = loader.get_template("administration/admin_produits_delete.html")
    context = {
        'produit': produit,
    }
    return HttpResponse(template.render(context, request=request))
