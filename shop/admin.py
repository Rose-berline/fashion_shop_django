from django.contrib import admin
from .models import Product, Category, CartItem, Wishlist
from shop.models import Promotion


# -------- Category Admin --------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


"""
Description :
Permet d'administrer les catégories dans Django Admin.
- list_display : colonnes affichées
- search_fields : barre de recherche
"""


# -------- Product Admin --------
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')


"""
Description :
Permet de gérer les produits.

Fonctions :
- Voir tous les produits
- Filtrer par catégorie
- Rechercher un produit
"""


# -------- Cart Admin --------
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')


"""
Description :
Permet de voir tous les paniers des utilisateurs.
"""


# -------- Wishlist Admin --------
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')


"""
Description :
Permet de voir les produits sauvegardés dans la wishlist.
"""


# -------- Register Models --------
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)

# Dans Django shell




