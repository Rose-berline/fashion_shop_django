from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import stripe
from .models import Product, Category, CartItem, Wishlist, Order, OrderItem, Promotion
from .forms import ProductForm, CategoryForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from shop.models import Profile

# ---------------- Stripe Configuration ----------------
stripe.api_key = settings.STRIPE_SECRET_KEY


# ---------------- Auth ----------------
@login_required
def logout_user(request):
    """Déconnecte l'utilisateur et redirige vers login."""
    logout(request)
    return redirect('login')


def register_user(request):
    """Inscription d'un nouvel utilisateur."""
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('login')
        else:
            messages.error(request, "Erreur lors de l'inscription. Vérifiez le formulaire.")
    return render(request, 'register.html', {'form': form})


def login_user(request):
    """
    Gère la connexion des utilisateurs.
    
    - POST : Authentifie et connecte l'utilisateur.
    - GET  : Affiche le formulaire de connexion.
    """

    if request.method == "POST":
        # Récupération des informations envoyées par le formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentifie l'utilisateur avec Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # L'utilisateur est authentifié → on le connecte
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")

            # Vérifie si l'utilisateur a déjà un profil, sinon on le crée
            Profile.objects.get_or_create(user=user)

            # Redirection selon le type d'utilisateur
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            # Authentification échouée
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            # Reste sur la page login pour réessayer
            return redirect('login')

    # Si GET, affiche le formulaire de connexion
    return render(request, "login.html", {})


# ---------------- Dashboard ----------------
@login_required
def dashboard(request):

    # ADMIN
    if request.user.is_superuser:

        total_products = Product.objects.count()
        total_categories = Category.objects.count()

        return render(request, 'dashboard_admin.html', {
            'total_products': total_products,
            'total_categories': total_categories
        })

    # UTILISATEUR NORMAL
    else:

        cart_items = CartItem.objects.filter(user=request.user).count()

        return render(request, 'dashboard_user.html', {
            'cart_items': cart_items
        })
    


@login_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    return render(request, 'dashboard_admin.html', {
        'total_products': total_products,
        'total_categories': total_categories
    })


# ---------------- Home ----------------
def home(request):
    """Page d'accueil avec produits filtrables, nouveautés et promotions."""
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    new_products = Product.objects.order_by('-id')[:8]
    promotions = Promotion.objects.filter(active=True)
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'new_products': new_products,
        'promotions': promotions
    }
    return render(request, 'home.html', context)


def home(request):
    products = Product.objects.all()
    wishlist_count = 0

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        'products': products,
        'wishlist_count': wishlist_count
    }

    return render(request, 'home.html', context)


# ---------------- Product CRUD ----------------
@login_required
def product_list(request):
    """Liste de tous les produits pour gestion."""
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def products(request):
    # ici tu peux envoyer les produits depuis la base
    context = {}
    return render(request, 'products.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


@login_required
def create_product(request):
    """Création d'un nouveau produit."""
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit créé avec succès !")
            return redirect('product_list')
        else:
            messages.error(request, "Erreur lors de la création du produit.")
    return render(request, 'product_form.html', {'form': form})


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, "Produit mis à jour avec succès !")
        return redirect('product_list')
    return render(request, 'product_form.html', {'form': form})


@login_required
def delete_product(request, id):
    """Supprime un produit existant."""
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Produit supprimé avec succès !")
    return redirect('product_list')


# ---------------- Category CRUD ----------------
@login_required
def category_list(request):
    """Affiche toutes les catégories et permet d'en créer une nouvelle."""
    categories = Category.objects.all()
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie ajoutée avec succès !")
            return redirect('category_list')
    return render(request, 'category.html', {'categories': categories, 'form': form})


@login_required
def category_update(request, id):
    """Met à jour une catégorie existante."""
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Catégorie mise à jour !")
        return redirect('category_list')
    return render(request, 'category.html', {'categories': Category.objects.all(), 'form': form})


@login_required
def category_delete(request, id):
    """Supprime une catégorie existante."""
    category = get_object_or_404(Category, id=id)
    category.delete()
    messages.success(request, "Catégorie supprimée !")
    return redirect('category_list')


# ---------------- Cart ----------------
@login_required
def cart(request):
    """Affiche le panier avec total."""
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    """Ajoute un produit au panier ou incrémente la quantité."""
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Produit ajouté au panier !")
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    """Supprime un produit spécifique du panier."""
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Produit retiré du panier.")
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    """Met à jour la quantité d'un item dans le panier."""
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == "POST":
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()
    messages.success(request, "Panier mis à jour.")
    return redirect('cart')


# ---------------- Profile ----------------
@login_required
def profile(request):
    """Affiche le profil de l'utilisateur."""
    return render(request, 'profile.html')


# ---------------- Contact ----------------
def contact(request):
    """Formulaire de contact et envoi d'email à l'admin."""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"Nouveau message de {name}"
        body = f"De : {name}\nEmail : {email}\n\nMessage :\n{message}"

        try:
            send_mail(subject, body, email, ['contact@complexe_wilo_store.com'], fail_silently=False)
            messages.success(request, "Merci ! Votre message a été envoyé avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi : {e}")

    return render(request, 'contact.html')


# ---------------- About ----------------
def about(request):
    """Page 'À propos'."""
    return render(request, 'about.html')


# ---------------- Checkout ----------------
@login_required
def checkout(request):
    """Crée une session Stripe pour le paiement."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Commande Fashion Shop'},
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return redirect(session.url)


@login_required
def success(request):
    """Finalisation de la commande après paiement."""
    cart = request.session.get('cart', {})
    order = Order.objects.create(user=request.user, paid=True)
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
    request.session['cart'] = {}
    return render(request, 'success.html')


# ---------------- Wishlist ----------------
@login_required
def add_wishlist(request, product_id):
    """Ajoute un produit à la wishlist."""
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, "Produit ajouté à votre wishlist !")
    return redirect('home')

@login_required
def wishlist(request):
    favorites = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'favorites': favorites})


@login_required
def remove_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()
    return redirect('wishlist')

# ---------------- Photos ----------------
def add_photo(request):
    return render(request, 'add_photo.html')


def delete_photo(request):
    return render(request, 'delete_photo.html')