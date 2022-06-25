import datetime
import json
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader

from accounts.models import User
from .models import Produit, Categorie, Commande, EstComposeDe, Panier


# Create your views here.
# @login_required mettre ça quand être login est necessaire
@login_required()
def account(request):
    template = loader.get_template("store/account.html")

    client = User.objects.get(id=request.user.id)
    commande = Commande.objects.filter(id_utilisateur=request.user.id, id_panier__valide=1).order_by("id_panier")
    produits = EstComposeDe.objects.all()
    context = {
        'client': client,
        'commande': commande,
        'produits': produits,
    }

    return HttpResponse(template.render(context, request=request))

def detail_commande(request, panier_id):
    template = loader.get_template("store/detail_commande.html")

    commande = Commande.objects.filter(id_utilisateur=request.user.id, id_panier=panier_id)
    if commande:
        if commande[0].id_panier.valide == 1:
            panier = EstComposeDe.objects.filter(id_panier=panier_id, id_panier__valide=1)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'commande': commande[0],
        'produits': panier,
    }

    return HttpResponse(template.render(context, request=request))

def index(request):
    template = loader.get_template("store/index.html")
    prods = Produit.objects.order_by("id")

    if request.user.is_superuser:
        template = loader.get_template("admin/admin_index.html")
        context = {}
        return HttpResponse(template.render(context, request=request))

    produits = []
    already_took = []
    for i in range(9):
        rand = random.randrange(0, len(prods))
        while rand in already_took and prods[rand].achetable == 0:
            rand = random.randrange(0, len(prods))

        already_took.append(rand)
        produits.append(prods[rand])

    context = {
        "produits": produits
    }

    return HttpResponse(template.render(context, request=request))


def rayon(request):
    template = loader.get_template("store/rayon.html")

    context = {
        'rayons': Categorie.objects.raw("SELECT * FROM commerce.categorie WHERE id IN (SELECT id_categorie FROM commerce.produit WHERE qtt_stock > 0) ORDER BY nom;")
    }

    return HttpResponse(template.render(context, request=request))


def rayon_listing(request, categorie_id):
    template = loader.get_template("store/rayon_listing.html")
    context = {
        'produits': Produit.objects.filter(categorie=categorie_id, achetable=1).order_by("nom").exclude(qtt_stock=0)
    }
    return HttpResponse(template.render(context, request=request))


def detail(request, produit_id):
    template = loader.get_template("store/detail.html")

    context = {
        'produit': Produit.objects.get(pk=produit_id)
    }
    return HttpResponse(template.render(context, request=request))


#@login_required()
def panier(request):
    template = loader.get_template("store/panier.html")

    if request.user.is_authenticated:
        client = User.objects.get(id=request.user.id)

        # SELECTION/CREATION COMMANDE ET PANIER
        commande = Commande.objects.filter(id_utilisateur=client.id, id_panier__valide=False)
        if commande:
            commande = commande[0]
            panier = commande.id_panier
        else:
            panier_id_max = Panier.objects.values_list('id').order_by('-id')
            if panier_id_max:
                panier = Panier.objects.create(id=panier_id_max[0][0] + 1)
            else:
                panier = Panier.objects.create(id=1)

            commande = Commande.objects.create(id_utilisateur=client, id_panier=panier)

        produits = EstComposeDe.objects.filter(id_panier=panier).order_by('id_produit__categorie')
    else:
        produits = []

    context = {
        'commande': commande,
        'produits': produits
    }
    return HttpResponse(template.render(context, request=request))

def ajout_panier(request, produit_id, produit_qtt):
    template = loader.get_template("store/detail.html")
    context = {
        'produit': Produit.objects.get(pk=produit_id),
        'quantite': produit_qtt
    }
    return HttpResponse(template.render(context, request=request))

def search(request):
    query = request.GET.get('query')
    if not query:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        produits = Produit.objects.filter(Q(nom__icontains=query) | Q(descript__icontains=query) | Q(marque__nom__icontains=query) | Q(categorie__nom__icontains=query)).filter(achetable=1).order_by("categorie")
        categories = Categorie.objects.filter(nom__icontains=query).order_by("id")
    context = {
        'query': query,
        'produits': produits,
        'categories':categories,
    }

    template = loader.get_template("store/search.html")
    return HttpResponse(template.render(context, request=request))

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    qtt = data['quantite']

    produit = Produit.objects.get(id=productId)
    client = User.objects.get(id=request.user.id)

    # SELECTION/CREATION COMMANDE ET PANIER
    commande = Commande.objects.filter(id_utilisateur=client.id, id_panier__valide=False)
    if commande:
        commande = commande[0]
        panier = commande.id_panier
    else:
        panier_id_max = Panier.objects.values_list('id').order_by('-id')
        if panier_id_max:
            panier = Panier.objects.create(id= panier_id_max[0][0] + 1)
        else:
            panier = Panier.objects.create(id=1)

        commande = Commande.objects.create(id_utilisateur=client, id_panier=panier)

    # SELECTION/CREATION COMPOSITION
    composition = EstComposeDe.objects.filter(id_produit=produit, id_panier=panier)
    if composition:
        composition = composition[0]
    else:
        composition = EstComposeDe.objects.create(id_produit=produit, id_panier=panier, quantite=0)

    quant = 0
    if action == "add":
        quant = composition.quantite + qtt
    elif action == "delete":
        quant = composition.quantite - 1

    if quant > composition.id_produit.qtt_stock:
        quant = composition.id_produit.qtt_stock

    with connection.cursor() as cursor:
        cursor.execute("UPDATE commerce.est_compose_de SET quantite=%s WHERE id_produit=%s AND id_panier=%s", [quant, composition.id_produit.id, composition.id_panier.id])

    if quant <= 0:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM commerce.est_compose_de WHERE id_produit=%s AND id_panier=%s AND quantite <= 0", [composition.id_produit.id, composition.id_panier.id])

    return JsonResponse("Article ajouté", safe=False)

def validerCommande(request):

    if request.user.is_authenticated:
        client = User.objects.get(id=request.user.id)
        commande = Commande.objects.get(id_utilisateur=client.id, id_panier__valide=False)
        if commande:
            panier = commande.id_panier
            composition = EstComposeDe.objects.filter(id_panier=panier).order_by('id_produit__categorie')
            for comp in composition:
                prod = comp.id_produit
                prod.qtt_stock = prod.qtt_stock - comp.quantite
                prod.save()

            panier.valide = 1
            panier.save()

            date = datetime.datetime.now()
            commande.date_validation = date.strftime("%Y-%m-%d %H:%M:%S")
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
                            <p>N° de commande: {panier.id}</p>
                            <p>Date de la commande: {date.strftime("%d/%m/%Y")}</p>
                    
                            <div class="container">
                                <div class="box-element">
                                    <h3>Détail de paiement :</h3>
                                    <table class="table">
                                        <tr>
                                            <th>
                                                <h5>Articles: <strong>{commande.get_cart_items}</strong> dont {len(composition)} différents
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

            for produit in composition:
                message += f"""
                <tr>
                <td><a href="{request.build_absolute_uri(f'/store/{produit.id_produit.id}')}"><img
                            src="{produit.id_produit.image}" alt="{produit.id_produit.nom}" height="75"
                            width="75"></a></td>
                <td>
                    <p>{produit.id_produit.nom}</p>
                </td>
                <td>
                    <p>{produit.id_produit.prix}€</p>
                </td>
                <td>
                    <p class="quantity">{produit.quantite}</p>
                </td>
                <td>
                    <p>{produit.calcPrixTotal}€</p>
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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

