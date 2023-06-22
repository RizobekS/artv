from django.urls import path
from . import views


app_name = "gallery"
urlpatterns = [
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('cart-count/', views.cart_items_count, name='cart_count'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-from-wishlist/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
