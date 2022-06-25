import json

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.template import loader

from accounts.models import User
from store.models import Produit, Marque, Categorie, Solide, Liquide, Unite


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    template = loader.get_template("admin/admin_index.html")

    context = {}

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def produits(request):
    template = loader.get_template("admin/admin_produits.html")

    produits = Produit.objects.filter(achetable=1).order_by("categorie__id")
    context = {
        'produits': produits
    }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def produits_ajouter(request):
    template = loader.get_template("admin/admin_produits_ajouter.html")

    marque = Marque.objects.all().order_by('nom')
    categorie = Categorie.objects.all().order_by('nom')

    context = {
        'marques': marque,
        'categories': categorie
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def ajouter(request):
    data = json.loads(request.body)

    if data["marque"] == "-1":
        id = Marque.objects.aggregate(Max('id'))['id__max'] + 1
        marque = Marque(id=id, nom=data["new_marque"])
        marque.save()
    else:
        marque = Marque.objects.get(pk=data["marque"])

    if data["categorie"] == "-1":
        id = Categorie.objects.aggregate(Max('id'))['id__max'] + 1
        categorie = Categorie(id=id, nom=data["new_categorie_nom"], tauxtva=data["new_categorie_tva"],
                              image=data["new_categorie_image"])
        categorie.save()
    else:
        categorie = Categorie.objects.get(pk=data["categorie"])

    id = Produit.objects.filter(categorie=categorie).aggregate(Max('id'))['id__max']
    if id:
        id = str(int(id[:id.find('_')]) + 1) + "_0"
    else:
        id = str(categorie.id * 10000 + 1) + "_0"

    new_prod = Produit(id=id, nom=data["nom"], prix=float(data["prix"]), qtt_stock=data["qtt_stock"],
                       descript=data["descript"], image=data["image"], marque=marque, categorie=categorie,
                       achetable=1)
    new_prod.save()

    if data["type"] == "0":
        type = Solide(id_prod=new_prod, kg=float(data["type_qtt"]))
    elif data["type"] == "1":
        type = Liquide(id_prod=new_prod, litre=float(data["type_qtt"]))
    else:
        type = Unite(id_prod=new_prod)

    type.save()

    return JsonResponse("Produit ajouté", safe=False)


@user_passes_test(lambda u: u.is_superuser)
def produits_detail(request, produit_id):
    template = loader.get_template("admin/admin_produits_detail.html")

    produit = Produit.objects.get(pk=produit_id)
    context = {
        'produit': produit
    }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def produits_modif(request, produit_id):
    produit = Produit.objects.get(pk=produit_id)

    if produit.achetable == 0:
        template = loader.get_template("admin/admin_produits_detail.html")
        context = {
            'produit': produit
        }
    else:
        template = loader.get_template("admin/admin_produits_modif.html")
        marque = Marque.objects.all().order_by('nom')
        categorie = Categorie.objects.all().order_by('nom')

        context = {
            'produit': produit,
            'marques': marque,
            'categories': categorie
        }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def produits_modif_stock(request, produit_id):
    produit = Produit.objects.get(pk=produit_id)

    if produit.achetable == 0:
        template = loader.get_template("admin/admin_produits_detail.html")
    else:
        template = loader.get_template("admin/admin_produits_modif_stock.html")

    context = {
        'produit': produit
    }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def update(request):
    data = json.loads(request.body)
    if data["changer"]:
        old_id = data["id"]

        old_prod = Produit.objects.get(pk=data["id"])
        old_prod.achetable = 0
        old_prod.save()

        if data["marque"] == "-1":
            id = Marque.objects.aggregate(Max('id'))['id__max'] + 1
            marque = Marque(id=id, nom=data["new_marque"])
            marque.save()
        else:
            marque = Marque.objects.get(pk=data["marque"])

        if data["categorie"] == "-1":
            id = Categorie.objects.aggregate(Max('id'))['id__max'] + 1
            categorie = Categorie(id=id, nom=data["new_categorie_nom"], tauxtva=data["new_categorie_tva"],
                                  image=data["new_categorie_image"])
            categorie.save()
        else:
            categorie = Categorie.objects.get(pk=data["categorie"])

        new_id = old_id[:(old_id.find('_') + 1)] + str(int(old_id[(old_id.find('_') + 1):]) + 1)
        new_prod = Produit(id=new_id, nom=data["nom"], prix=float(data["prix"]), qtt_stock=data["qtt_stock"],
                           descript=data["descript"], image=data["image"], marque=marque, categorie=categorie,
                           achetable=1)
        new_prod.save()

        if data["type"] == "0":
            type = Solide(id_prod=new_prod, kg=float(data["type_qtt"]))
        elif data["type"] == "1":
            type = Liquide(id_prod=new_prod, litre=float(data["type_qtt"]))
        else:
            type = Unite(id_prod=new_prod)

        type.save()

    return JsonResponse("Produit modifié", safe=False)


@user_passes_test(lambda u: u.is_superuser)
def updateQtt(request):
    data = json.loads(request.body)
    id = data['prod_id']
    qtt = data['quantite']

    produit = Produit.objects.get(pk=id)
    produit.qtt_stock = qtt
    produit.save()
    return JsonResponse("Quantité modifiée", safe=False)


@user_passes_test(lambda u: u.is_superuser)
def delete(request):
    data = json.loads(request.body)
    id = data["id"]

    produit = Produit.objects.get(pk=id)
    produit.achetable = 0
    produit.save()
    return JsonResponse("Produit supprimé", safe=False)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    template = loader.get_template("admin/admin_categories.html")

    categories = Categorie.objects.all()
    context = {
        'categories': categories
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def ajouter_categories(request):
    template = loader.get_template("admin/admin_categories_ajouter.html")

    context = {}

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def add_categories(request):
    data = json.loads(request.body)
    id = Categorie.objects.all().aggregate(Max('id'))['id__max'] + 1
    categorie = Categorie(id=id, nom=data["nom"], tauxtva=data["tva"], image=data["image"])
    categorie.save()
    return JsonResponse("Catégorie ajouté", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def modifier_categories(request, id):
    template = loader.get_template("admin/admin_categories_modif.html")
    categorie = Categorie.objects.get(pk=id)
    context = {
        'categorie': categorie
    }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def update_categories(request):
    data = json.loads(request.body)
    if data["changer"]:
        categorie = Categorie.objects.get(pk=data["id"])
        categorie.nom = data["nom"]
        categorie.tauxtva = float(data["tva"])
        categorie.image = data["image"]
        categorie.save()
    return JsonResponse("Catégorie modifiéé", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def delete_categories(request, id):
    template = loader.get_template("admin/admin_categories_delete.html")

    categorie = Categorie.objects.get(pk=id)
    produits = Produit.objects.filter(categorie=categorie)
    context = {
        'categorie': categorie,
        'produits': produits
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def suppr_categories(request):
    data = json.loads(request.body)
    categorie = Categorie.objects.get(pk=data["id"])
    categorie.delete()
    return JsonResponse("Catégorie supprimée", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def marques(request):
    template = loader.get_template("admin/admin_marques.html")

    marques = Marque.objects.all()
    context = {
        'marques': marques
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def ajouter_marques(request):
    template = loader.get_template("admin/admin_marques_ajouter.html")

    context = {}

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def add_marques(request):
    data = json.loads(request.body)
    id = Marque.objects.all().aggregate(Max('id'))['id__max'] + 1
    marque = Marque(id=id, nom=data["nom"])
    marque.save()
    return JsonResponse("Marque ajouté", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def modifier_marques(request, id):
    template = loader.get_template("admin/admin_marques_modif.html")
    marque = Marque.objects.get(pk=id)
    context = {
        'marque': marque
    }

    return HttpResponse(template.render(context, request=request))


@user_passes_test(lambda u: u.is_superuser)
def update_marques(request):
    data = json.loads(request.body)
    if data["changer"]:
        marque = Marque.objects.get(pk=data["id"])
        marque.nom = data["nom"]
        marque.save()
    return JsonResponse("Marque modifiéé", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def delete_marques(request, id):
    template = loader.get_template("admin/admin_marques_delete.html")

    marque = Marque.objects.get(pk=id)
    produits = Produit.objects.filter(marque=marque)

    context = {
        'marque': marque,
        'produits': produits
    }

    return HttpResponse(template.render(context, request=request))

@user_passes_test(lambda u: u.is_superuser)
def suppr_marques(request):
    data = json.loads(request.body)
    marque = Marque.objects.get(pk=data["id"])
    marque.delete()
    return JsonResponse("Marque supprimée", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def clients(request):
    template = loader.get_template("admin/admin_clients.html")

    clients = User.objects.filter(is_superuser=0).order_by("id")
    context = {
        'clients': clients
    }

    return HttpResponse(template.render(context, request=request))
