import datetime
import json
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template import loader

from store.models import Produit, Categorie, Commande, Commande_Produit

User = get_user_model()


@login_required()
def account(request):
    client = User.objects.get(id=request.user.id)
    commandes = Commande.objects.filter(utilisateur=request.user.id, est_complete=1).order_by("id")

    template = loader.get_template("store/account.html")
    context = {
        'client': client,
        'commandes': commandes
    }

    return HttpResponse(template.render(context, request=request))

@login_required()
def historiqueCommande(request, id):
    commande = get_object_or_404(Commande, id=id, utilisateur=request.user.id, est_complete=1)
    produits = Commande_Produit.objects.filter(commande=commande).order_by('produit__categorie')

    template = loader.get_template("store/historiqueCommande.html")
    context = {
        "commande": commande,
        "produits": produits
    }
    return HttpResponse(template.render(context, request=request))

def index(request):
    if request.user.is_superuser:
        return redirect('administration:index')

    prods = Produit.objects.order_by("id")
    produits = []
    already_took = []
    for i in range(5):
        rand = random.randrange(0, len(prods))
        while rand in already_took or prods[rand].achetable == 0:
            rand = random.randrange(0, len(prods))

        already_took.append(rand)
        produits.append(prods[rand])

    template = loader.get_template("store/index.html")
    context = {
        "produits": produits
    }

    return HttpResponse(template.render(context, request=request))

def panier(request):
    if request.user.is_authenticated:
        client = User.objects.get(id=request.user.id)

        commande = Commande.objects.get_or_create(utilisateur=client, est_complete=0)[0]
        produits = Commande_Produit.objects.filter(commande=commande).order_by('produit__categorie')

        if request.method == "POST":
            for comp in produits:
                prod = comp.produit
                prod.stock = prod.stock - comp.quantite
                prod.save()

            commande.est_complete = 1
            date = datetime.datetime.now()
            commande.date_commande = date.strftime("%Y-%m-%d %H:%M:%S")
            commande.save()

            sujet = "Merci pour votre commande !"
            message = """<!DOCTYPE html>
                                    <html lang="en">

                                    <head>
                                        <meta charset="UTF-8">
                                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <title>Merci pour votre commande !</title>
                                        <style>
                                            .box-element {
                                                box-shadow: hsl(0, 0%, 80%) 0 0 16px;
                                                background-color: #fff;
                                                border-radius: 4px;
                                                padding: 10px;
                                            }

                                            .row-image {
                                                width: 100px;
                                            }

                                            .cart-row {
                                                display: flex;
                                                align-items: flex-stretch;
                                                padding-bottom: 10px;
                                                margin-bottom: 10px;
                                                border-bottom: 1px solid #ececec;

                                            }

                                            .quantity {
                                                display: inline-block;
                                                font-weight: 700;
                                                padding-right: 10px;


                                            }

                                            .chg-quantity {
                                                width: 12px;
                                                cursor: pointer;
                                                display: block;
                                                margin-top: 5px;
                                                transition: .1s;
                                            }

                                            .chg-quantity:hover {
                                                opacity: .6;
                                            }

                                            table {
                                                table-layout: fixed;
                                                width: 100%;
                                            }

                                            td {
                                                text-align: center;
                                            }

                                            .bg-noir {
                                                color: #fff;
                                                background-color: black;
                                                text-align: center;
                                                padding: 2px;
                                            }

                                            .bg-gris {
                                                background-color: rgb(230, 230, 230);
                                                text-align: center;
                                                padding: 2px;
                                            }

                                            .container {
                                                padding: 10px;
                                            }

                                            h3 {
                                                text-align: left;
                                            }
                                        </style>
                                    </head> """ + f"""
                                    <body>
                                    <div class="bg-noir">
                                        <h1>Bio & Terre</h1>
                                    </div>
                                    <div class="bg-gris">
                                        <h2>VOTRE COMMANDE EST ENREGISTRÉE !</h2>

                                        <p>Bonjour {client.first_name.capitalize()}, votre commande a été reçue et nous vous en remercions.</p>
                                        <p>N° de commande: {commande.id}</p>
                                        <p>Date de la commande: {date.strftime("%d/%m/%Y")}</p>

                                        <div class="container">
                                            <div class="box-element">
                                                <h3>Détail de paiement :</h3>
                                                <table class="table">
                                                    <tr>
                                                        <th>
                                                            <h5>Articles: <strong>{commande.get_cart_items}</strong> dont {len(produits)} différents
                                                            </h5>
                                                        </th>
                                                        <th>
                                                            <h5>Total: <strong>{commande.get_cart_total}€</strong></h5>
                                                        </th>
                                                        <th></th>
                                                    </tr>
                                                </table>
                                            </div>

                                            <br>

                                            <div class="box-element">
                                                <h3>Détail de commande :</h3>
                                                <table>
                                                    <tr>
                                                        <th>Image</th>
                                                        <th>Article</th>
                                                        <th>Prix</th>
                                                        <th>Quantité</th>
                                                        <th>Total</th>
                                                    </tr>"""

            for commande_produit in produits:
                message += f"""
                            <tr>
                            <td><a href="{request.build_absolute_uri(f'/store/produit/{commande_produit.produit.id}')}"><img
                                        src="{commande_produit.produit.image}" alt="{commande_produit.produit.nom}" height="75"
                                        width="75"></a></td>
                            <td>
                                <p>{commande_produit.produit.nom}</p>
                            </td>
                            <td>
                                <p>{commande_produit.produit.prix}€</p>
                            </td>
                            <td>
                                <p class="quantity">{commande_produit.quantite}</p>
                            </td>
                            <td>
                                <p>{commande_produit.calcPrixTotal}€</p>
                            </td>
                            </tr>
                            """

            message += """</table>
                                    </div><br>
                                </div>

                                <p>Cordialement,</p>
                                <p><strong>L'équipe de Bio & Terre</strong></p>
                            </div>
                        </body>

                        </html>"""

            envoyeur = settings.EMAIL_HOST_USER
            destinataire = [client.email]

            email = EmailMessage(sujet, message, envoyeur, destinataire)
            email.content_subtype = "html"
            email.send()

            messages.error(request, "Toute l’équipe de Bio&Terre vous remercie pour votre commande !")
            messages.error(request, f"Un mail récapitulant votre commande vient de vous être envoyé à l’adresse mail suivante : {client.email}.")

            return redirect('store:panier')
    else:
        commande = []
        produits = []

    template = loader.get_template("store/panier.html")
    context = {
        'commande': commande,
        'produits': produits
    }
    return HttpResponse(template.render(context, request=request))

def panierModifierQuantite(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    produit = Produit.objects.get(id=productId)
    client = User.objects.get(id=request.user.id)

    commande = Commande.objects.get_or_create(utilisateur=client, est_complete=0)[0]
    composition = Commande_Produit.objects.filter(produit=produit, commande=commande)[0]

    quant = 0
    if action == "add":
        quant = composition.quantite + 1
    elif action == "delete":
        quant = composition.quantite - 1

    if quant > composition.produit.stock:
        quant = composition.produit.stock

    if quant > 0:
        composition.quantite = quant
        composition.save()
    else:
        composition.delete()

    return JsonResponse("Quantité modifiée", safe=False)

def rayons(request):
    if request.user.is_superuser:
        return redirect('administration:index')

    template = loader.get_template("store/rayons.html")
    rayons = Categorie.objects.order_by("nom")
    context = {
        "rayons": rayons,
    }
    return HttpResponse(template.render(context, request=request))

def rayons_listing(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    template = loader.get_template("store/rayon_listing.html")

    if request.method == 'GET':
        if request.GET.get('q'):
            produits = Produit.objects.filter(categorie=id, achetable=1).order_by(request.GET.get('q')).exclude(stock=0)
        else:
            produits = Produit.objects.filter(categorie=id, achetable=1).order_by("nom").exclude(stock=0)

    context = {
        'produits': produits
    }
    return HttpResponse(template.render(context, request=request))

def recherche(request):
    query = request.GET.get('query')

    if not query:
        return redirect('index')

    produits = Produit.objects.filter(
        Q(nom__icontains=query) | Q(description__icontains=query) | Q(marque__nom__icontains=query) | Q(
            categorie__nom__icontains=query)).filter(achetable=1).order_by("categorie")
    categories = Categorie.objects.filter(nom__icontains=query).order_by("id")

    context = {
        'query': query,
        'produits': produits,
        'categories': categories,
    }
    template = loader.get_template("store/recherche.html")
    return HttpResponse(template.render(context, request=request))

def produit_detail(request, id):
    produit = get_object_or_404(Produit, id=id)

    if request.method == "POST":
        quantite = int(request.POST.get("quantite"))
        if request.user.is_authenticated:
            produit = Produit.objects.get(id=id)
            client = User.objects.get(id=request.user.id)

            commande = Commande.objects.get_or_create(utilisateur=client, est_complete=0)[0]
            commande_produit = Commande_Produit.objects.filter(commande=commande.id, produit=produit.id)
            if commande_produit:
                commande_produit = commande_produit[0]
                commande_produit.quantite += quantite
                commande_produit.save()
            else:
                commande_produit = Commande_Produit.objects.create(commande=commande, produit=produit, quantite=quantite)

            if quantite == 1:
                messages.error(request, f"{quantite} '{produit.nom}' a été ajouté à votre panier.")
            else:
                messages.error(request, f"{quantite} '{produit.nom}' ont été ajoutés à votre panier.")

    template = loader.get_template("store/produit_detail.html")
    context = {
        'produit': produit,
    }
    return HttpResponse(template.render(context, request=request))