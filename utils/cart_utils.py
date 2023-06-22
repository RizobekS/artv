from gallery.models import Cart, CartItemChoices


def get_cart_items_count(user):
	cart_items = 0
	if user.is_anonymous:
		pass
	else:
		try:
			cart = Cart.objects.get(user__email=user.email)
			cart_items = 0
			for item in cart.cart_items.all():
				if item.status == CartItemChoices.CART_CART:
					cart_items += 1
		except Cart.DoesNotExist:
			pass
		except:
			pass
	return cart_items
