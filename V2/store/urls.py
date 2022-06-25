from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('account/', views.account, name="account"),
    path('histCommande/<int:id>', views.historiqueCommande, name="historiqueCommande"),
    path('panier/', views.panier, name="panier"),
    path('panierModifQtt/', views.panierModifierQuantite, name="panierModifierQuantite"),
    path('rayons/', views.rayons, name="rayons"),
    path('rayons/<int:id>', views.rayons_listing, name="rayon_listing"),
    path('recherche/', views.recherche, name="recherche"),
    path('produit/<str:id>', views.produit_detail, name="produit_detail"),
]