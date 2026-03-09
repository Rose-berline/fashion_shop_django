from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




# ---------------- Profile ----------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png')

    def __str__(self):
        return self.user.username





# ---------------- Category ----------------
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


"""
Description :
Cette table représente les catégories de produits.
Exemples : Chemises, Pantalons, Chaussures, Accessoires.

Chaque produit appartient à une catégorie.
"""


# ---------------- Product ----------------
class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    image = models.ImageField(upload_to='products/', blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


"""
Description :
Cette table représente les produits du magasin.

Champs :
- name : nom du produit
- description : description du produit
- price : prix
- image : image du produit
- category : catégorie du produit
- created_at : date d'ajout du produit
"""


# ---------------- Cart ----------------
class CartItem(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


"""
Description :
Cette table représente le panier d’un utilisateur.

Champs :
- user : utilisateur qui possède le panier
- product : produit ajouté au panier
- quantity : quantité du produit

Méthode :
- total_price() : calcule le prix total pour cet article
"""


# ---------------- Wishlist ----------------
class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


"""
Description :
Cette table représente la liste de souhaits (wishlist).

Un utilisateur peut sauvegarder des produits
pour les acheter plus tard.
"""


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Commande {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity


class Promotion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='promotions/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

