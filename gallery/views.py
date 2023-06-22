import json

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from accounts.models import AuthUsers
from utils.cart_utils import get_cart_items_count
from gallery.models import Order, StatusChoices, AppliedArt
from gallery.models import Cart, Works, CartItemChoices, CartItem


@login_required()
def add_to_wishlist(request, slug):
    try:
        cart = Cart.objects.get(user__email__exact=request.user.email)
    except Cart.DoesNotExist:
        auth_user = AuthUsers.objects.get(email=request.user.email)
        cart = Cart.objects.create(user=auth_user)

    if Works.objects.filter(slug=slug).exists():
        art_work = Works.objects.get(slug=slug)

        if cart.cart_items.filter(art_work=art_work, status=CartItemChoices.CART_WISHLIST).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                art_work=art_work, status=CartItemChoices.CART_WISHLIST)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            messages.success(request, 'Товар был удален из списка желаний')
            return HttpResponse(status=204)
        else:
            if art_work.status == StatusChoices.SOLD:
                messages.error(request, f"Ошибка! Товар уже продан.")
                return HttpResponse(status=404)
            else:
                cart.cart_items.create(art_work=art_work, status=CartItemChoices.CART_WISHLIST)
                messages.success(request, 'Произведение добавлено в список желаний')
                return HttpResponse(status=201)

    elif AppliedArt.objects.filter(slug=slug).exists():
        art_work = AppliedArt.objects.get(slug=slug)
        if cart.cart_items.filter(applied_art=art_work, status=CartItemChoices.CART_WISHLIST).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                applied_art=art_work, status=CartItemChoices.CART_WISHLIST)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            messages.success(request, 'Товар был удален из списка желаний')
            return HttpResponse(status=204)
        else:
            if art_work.status == StatusChoices.SOLD:
                messages.error(request, f"Ошибка! Товар уже продан.")
                return HttpResponse(status=404)
            else:
                cart.cart_items.create(applied_art=art_work, is_applied_art=True, status=CartItemChoices.CART_WISHLIST)
                messages.success(request, 'Товар добавлен в список желаний')
                return HttpResponse(status=201)


@login_required()
def add_to_cart(request, slug):
    try:
        cart = Cart.objects.get(user__email__exact=request.user.email)
    except Cart.DoesNotExist:
        auth_user = AuthUsers.objects.get(email=request.user.email)
        cart = Cart.objects.create(user=auth_user)

    if Works.objects.filter(slug=slug).exists():
        art_work = Works.objects.get(slug=slug)
        if art_work.status == StatusChoices.SOLD:
            messages.error(request, f"Ошибка! Товар уже продан.")
            return HttpResponse(status=404)

        if cart.cart_items.filter(art_work=art_work, status=CartItemChoices.CART_CART).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                art_work=art_work, status=CartItemChoices.CART_CART)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            get_cart_items_count(request.user)
            messages.success(request, 'Удалено из корзины')
            return HttpResponse(status=204)
        else:
            cart.cart_items.create(art_work=art_work, status=CartItemChoices.CART_CART)
            messages.success(request, 'Товар был добавлен в корзину')
            return HttpResponse(status=201)

    elif AppliedArt.objects.filter(slug=slug).exists():
        art_work = AppliedArt.objects.get(slug=slug)

        if art_work.status == StatusChoices.SOLD:
            messages.error(request, f"Ошибка! Товар уже продан.")
            return HttpResponse(status=404)

        if cart.cart_items.filter(applied_art=art_work, status=CartItemChoices.CART_CART).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                applied_art=art_work, status=CartItemChoices.CART_CART)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            get_cart_items_count(request.user)
            messages.success(request, 'Удалено из корзины')
            return HttpResponse(status=204)
        else:
            cart.cart_items.create(applied_art=art_work, is_applied_art=True, status=CartItemChoices.CART_CART)
            messages.success(request, 'Товар был добавлен в корзину')
            return HttpResponse(status=201)


@login_required()
@require_http_methods(["DELETE"])
def remove_from_wishlist(request, slug):
    cart = Cart.objects.get(user__email=request.user.email)

    if Works.objects.filter(slug=slug).exists():
        art_work = Works.objects.get(slug=slug)

        if cart.cart_items.filter(art_work=art_work, status=CartItemChoices.CART_WISHLIST).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                art_work=art_work, status=CartItemChoices.CART_WISHLIST)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            messages.success(request, 'Товар был удален из списка желаний')
            return HttpResponse(status=204)
        return HttpResponse(status=404)

    elif AppliedArt.objects.filter(slug=slug).exists():
        art_work = AppliedArt.objects.get(slug=slug)

        if cart.cart_items.filter(applied_art=art_work, status=CartItemChoices.CART_WISHLIST).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                applied_art=art_work, status=CartItemChoices.CART_WISHLIST)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            messages.success(request, 'Товар был удален из списка желаний')
            return HttpResponse(status=204)
        return HttpResponse(status=404)


@login_required()
@require_http_methods(["DELETE"])
def remove_from_cart(request, slug):
    cart = Cart.objects.get(user__email=request.user.email)

    if Works.objects.filter(slug=slug).exists():
        art_work = Works.objects.get(slug=slug)

        if cart.cart_items.filter(art_work=art_work, status=CartItemChoices.CART_CART).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                art_work=art_work, status=CartItemChoices.CART_CART)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            get_cart_items_count(request.user)
            messages.success(request, 'Удалено из корзины')
        return HttpResponse(status=204)

    elif AppliedArt.objects.filter(slug=slug).exists():
        art_work = AppliedArt.objects.get(slug=slug)

        if cart.cart_items.filter(applied_art=art_work, status=CartItemChoices.CART_CART).exists():
            cart_item = CartItem.objects.filter(cart=cart).get(
                applied_art=art_work, status=CartItemChoices.CART_CART)
            cart.cart_items.remove(cart_item)
            cart_item.delete()
            get_cart_items_count(request.user)
            messages.success(request, 'Удалено из корзины')

        return HttpResponse(status=204)
    return HttpResponse(status=404)


@login_required()
def clear_cart(request):
    try:
        cart = Cart.objects.get(user__email=request.user.email)
        cart.cart_items.filter(status=CartItemChoices.CART_CART).delete()
        count = get_cart_items_count(request.user)
        messages.success(request, 'Корзина очищена')
        return JsonResponse(status=204, data={'cart_items': count})
    except Exception as e:
        print(e)
        return HttpResponse(status=404)


@login_required()
def cart_items_count(request):
    cart_items = get_cart_items_count(request.user)

    response_data = {"cart_items": cart_items}

    return HttpResponse(json.dumps(response_data), content_type="application/json")