from .cart import Cart


def cart_summary(request):
    try:
        cart = Cart(request)
        count = sum(item['quantity'] for item in cart.items())
        total = cart.total()
        discount_pct = int(request.session.get('discount_pct', 0))
        discounted_total = total - (total * discount_pct / 100) if discount_pct else total
        wishlist_ids = request.session.get('wishlist', [])
    except Exception:
        count = 0
        total = 0
        discount_pct = 0
        discounted_total = 0
        wishlist_ids = []
    return {
        'cart_count': count,
        'cart_total': total,
        'cart_discount_pct': discount_pct,
        'cart_discounted_total': discounted_total,
        'wishlist_ids': wishlist_ids,
    }


