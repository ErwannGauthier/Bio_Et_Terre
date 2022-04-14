from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    url(r'^rayon/$', views.rayon, name='rayon'),
    url(r'^rayon/(?P<categorie_id>[0-9]+)/$', views.rayon_listing, name='rayon_listing'),
    url(r'^(?P<produit_id>[0-9]+_[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<produit_id>[0-9]+_[0-9]+)/(?P<produit_qtt>[0-9]+)$', views.ajout_panier, name='ajout_panier'),
    url(r'^panier/', views.panier, name="panier"),
    url(r'^search/$', views.search, name='search'),
    path('update_item/', views.updateItem, name="update_item"),
    path('valider_commande/', views.validerCommande, name="valider_commande"),
    path('account/', views.account, name="account"),
    url('^account/detail_commande/(?P<panier_id>[0-9]+)$', views.detail_commande, name="detail_commande")
]