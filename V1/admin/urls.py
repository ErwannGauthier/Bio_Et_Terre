from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'admin'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('produits/', views.produits, name="produits"),
    path('produits/ajouter/', views.produits_ajouter, name="produits_ajouter"),
    url(r'^produits/(?P<produit_id>[0-9]+_[0-9]+)/$', views.produits_detail, name='produits_detail'),
    url(r'^produits/modif/(?P<produit_id>[0-9]+_[0-9]+)/$', views.produits_modif, name='produits_modif'),
    url(r'^produits/modif_stock/(?P<produit_id>[0-9]+_[0-9]+)/$', views.produits_modif_stock, name='produits_modif_stock'),
    path('updateQtt/', views.updateQtt, name="updateQtt"),
    path('update/', views.update, name="update"),
    path('ajouter/', views.ajouter, name="ajouter"),
    path('delete/', views.delete, name="delete"),
    path('categories/', views.categories, name='categories'),
    path('categories/ajouter/', views.ajouter_categories, name='ajouter_categories'),
    path('categories_add/', views.add_categories, name='add_categories'),
    url(r'^categories/modif/(?P<id>[0-9]+)/$', views.modifier_categories, name='modifier_categories'),
    path('update_categorie/', views.update_categories, name='update_categories'),
    url(r'^categories/suppr/(?P<id>[0-9]+)/$', views.delete_categories, name='delete_categories'),
    path('categories/suppr/', views.suppr_categories, name='suppr_categories'),
    path('marques/', views.marques, name='marques'),
    path('marques/ajouter/', views.ajouter_marques, name='ajouter_marques'),
    path('marques_add/', views.add_marques, name='add_marques'),
    url(r'^marques/modif/(?P<id>[0-9]+)/$', views.modifier_marques, name='modifier_marques'),
    path('update_marque/', views.update_marques, name='update_marques'),
    url(r'^marques/suppr/(?P<id>[0-9]+)/$', views.delete_marques, name='delete_marques'),
    path('marques/suppr/', views.suppr_marques, name='suppr_marques'),
    path('clients/', views.clients, name="clients"),
]