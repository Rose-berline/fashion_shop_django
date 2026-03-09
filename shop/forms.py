from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category


# -------- User Register Form --------
class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


"""
Description :
Formulaire pour créer un compte utilisateur.

Champs :
- username
- email
- password1
- password2
"""


# -------- Category Form --------
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']


"""
Description :
Formulaire pour créer ou modifier une catégorie.
"""


# -------- Product Form --------
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'image',
            'category'
        ]


"""
Description :
Formulaire pour ajouter ou modifier un produit.

Champs :
- name
- description
- price
- image
- category
"""