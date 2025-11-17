from decimal import Decimal
from .models import Dish


CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(CART_SESSION_KEY, {})

    def add(self, dish_id: int, qty: int = 1):
        self.cart[str(dish_id)] = self.cart.get(str(dish_id), 0) + qty
        self.save()

    def decrement(self, dish_id: int, qty: int = 1):
        key = str(dish_id)
        if key in self.cart:
            new_qty = int(self.cart[key]) - qty
            if new_qty > 0:
                self.cart[key] = new_qty
            else:
                self.cart
            self.save()

    def remove(self, dish_id: int):
        self.cart.pop(str(dish_id), None)
        self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.session.modified = True

    def items(self):
        dish_ids = [int(i) for i in self.cart.keys()]
        dishes = {d.id: d for d in Dish.objects.filter(id__in=dish_ids, is_active=True)}
        for sid, qty in self.cart.items():
            d = dishes.get(int(sid))
            if d:
                yield {
                    'dish': d,
                    'quantity': qty,
                    'unit_price': d.price,
                    'subtotal': Decimal(qty) * d.price,
                }

    def total(self):
        return sum(i['subtotal'] for i in self.items())

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True


