from django.urls import path

from . import views

app_name = 'administration'

urlpatterns = [
    path('index/', views.index, name="index"),

    path('categories/', views.categories, name='categories'),
    path('categories/ajouter/', views.categories_ajouter, name='categories_ajouter'),
    path('categories/modif/<str:id>/', views.categories_modifier, name='categories_modifier'),
    path('categories/suppr/<str:id>/', views.categories_supprimer, name='categories_supprimer'),

    path('clients/', views.clients, name="clients"),

    path('marques/', views.marques, name='marques'),
    path('marques/ajouter/', views.marques_ajouter, name='marques_ajouter'),
    path('marques/modif/<str:id>/', views.marques_modifier, name='marques_modifier'),
    path('marques/suppr/<str:id>/', views.marques_supprimer, name='marques_supprimer'),

    path('produits/', views.produits, name="produits"),
    path('produits/ajouter/', views.produits_ajouter, name="produits_ajouter"),
    path('produits/<str:id>/', views.produits_detail, name='produits_detail'),
    path('produits/modif/<str:id>/', views.produits_modifier, name='produits_modifier'),
    path('produits/modif_stock/<str:id>/', views.produits_modifier_stock, name='produits_modifier_stock'),
    path('produits/suppr/<str:id>/', views.produits_supprimer, name='produits_supprimer'),
]