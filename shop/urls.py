from django.urls import path
from . import views

urlpatterns = [
    # ---------------- Auth ----------------
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # ---------------- Dashboard ----------------
    path('dashboard/', views.dashboard, name='dashboard'),  # pour utilisateurs normaux
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), # si tu veux l'admin

    # ---------------- Home ----------------
    path('', views.home, name='home'),

    # ---------------- Product CRUD ----------------
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.create_product, name='create_product'),
    path('products/<int:pk>/edit/', views.update_product, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # ---------------- Category CRUD ----------------
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:id>/update/', views.category_update, name='category_update'),
    path('categories/<int:id>/delete/', views.category_delete, name='category_delete'),

    # ---------------- Cart ----------------
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    # ---------------- Profile ----------------
    path('profile/', views.profile, name='profile'),

    # ---------------- Contact & About ----------------
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    # ---------------- Checkout ----------------
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),

    # ---------------- Wishlist ----------------
    path('wishlist/add/<int:product_id>/', views.add_wishlist, name='add_wishlist'),

    # ---------------- Photos ----------------
    path('add-photo/', views.add_photo, name='add_photo'),
    path('delete-photo/', views.delete_photo, name='delete_photo'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-wishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
]