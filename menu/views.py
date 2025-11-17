from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import SignupForm
from .models import Dish, Order, OrderItem, DeliveryZone
from django.db.models import Max
from .cart import Cart
from decimal import Decimal


def menu_list(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q')
    f = request.GET.get('f', 'all')
    cat = request.GET.get('cat')
    dishes = Dish.objects.filter(is_active=True)
    if q:
        dishes = dishes.filter(name__icontains=q) | dishes.filter(description__icontains=q)
    if cat in {c.value for c in Dish.Category}:
        dishes = dishes.filter(category=cat)
    if f == 'newcomers':
        dishes = dishes.order_by('-created_at')
    elif f == 'best':
        dishes = dishes.filter(is_best_seller=True)
    elif f == 'top':
        dishes = dishes.order_by('-rating')
    context = {"dishes": dishes, "active_filter": f, "active_category": cat}
    return render(request, 'menu/menu_list.html', context)


def dish_detail(request: HttpRequest, pk: int) -> HttpResponse:
    dish = get_object_or_404(Dish, pk=pk, is_active=True)
    return render(request, 'menu/dish_detail.html', {"dish": dish})


def cart_view(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    delivery_fee = Decimal(request.session.get('delivery_fee', 0))
    total_with_delivery = cart.total() + delivery_fee
    return render(request, 'menu/cart.html', {"cart": cart,"delivery_fee": delivery_fee,
        "total_with_delivery": total_with_delivery,})


def cart_add(request: HttpRequest, pk: int) -> HttpResponse:
    cart = Cart(request)
    cart.add(pk, 1)
    # Detect AJAX requests; if AJAX, return JSON and do NOT add a Django message
    requested_with = (request.headers.get('x-requested-with') or request.META.get('HTTP_X_REQUESTED_WITH') or '')
    accept_hdr = request.META.get('HTTP_ACCEPT', '') or ''
    is_ajax = (requested_with == 'XMLHttpRequest') or ('application/json' in accept_hdr)

    # compute total items in cart
    try:
        cart_count = sum(int(v) for v in cart.cart.values())
    except Exception:
        cart_count = 0

    if is_ajax:
        # compute item quantity and subtotal
        qty = int(cart.cart.get(str(pk), 0))
        try:
            dish = Dish.objects.get(pk=pk)
            item_subtotal = str(dish.price * qty)
        except Exception:
            item_subtotal = '0.00'
        return JsonResponse({
            'status': 'ok',
            'message': 'Added to cart',
            'cart_count': cart_count,
            'dish_id': pk,
            'item_quantity': qty,
            'item_subtotal': item_subtotal,
            'cart_total': str(cart.total()),
        })

    # Non-AJAX fallback: add Django message and redirect
    messages.success(request, "Added to cart")
    return redirect(request.META.get('HTTP_REFERER') or reverse('menu:menu_list'))


def cart_remove(request: HttpRequest, pk: int) -> HttpResponse:
    cart = Cart(request)
    cart.remove(pk)
    # Detect AJAX and return JSON for client-side updates
    requested_with = (request.headers.get('x-requested-with') or request.META.get('HTTP_X_REQUESTED_WITH') or '')
    accept_hdr = request.META.get('HTTP_ACCEPT', '') or ''
    is_ajax = (requested_with == 'XMLHttpRequest') or ('application/json' in accept_hdr)

    # compute cart_count and total
    try:
        cart_count = sum(int(v) for v in cart.cart.values())
    except Exception:
        cart_count = 0

    if is_ajax:
        return JsonResponse({
            'status': 'ok',
            'message': 'Removed from cart',
            'cart_count': cart_count,
            'cart_total': str(cart.total()),
            'item_quantity': 0,
            'item_subtotal': '0.00',
            'dish_id': pk,
        })

    messages.info(request, "Removed from cart")
    return redirect('menu:cart')


def cart_decrement(request: HttpRequest, pk: int) -> HttpResponse:
    cart = Cart(request)
    cart.decrement(pk, 1)
    # Detect AJAX and return JSON for client-side updates
    requested_with = (request.headers.get('x-requested-with') or request.META.get('HTTP_X_REQUESTED_WITH') or '')
    accept_hdr = request.META.get('HTTP_ACCEPT', '') or ''
    is_ajax = (requested_with == 'XMLHttpRequest') or ('application/json' in accept_hdr)

    try:
        cart_count = sum(int(v) for v in cart.cart.values())
    except Exception:
        cart_count = 0

    # get remaining quantity for this dish
    qty = int(cart.cart.get(str(pk), 0))
    # compute item subtotal if possible
    try:
        dish = Dish.objects.get(pk=pk)
        item_subtotal = str(dish.price * qty)
    except Exception:
        item_subtotal = '0.00'

    if is_ajax:
        return JsonResponse({
            'status': 'ok',
            'message': 'Quantity updated',
            'cart_count': cart_count,
            'cart_total': str(cart.total()),
            'item_quantity': qty,
            'item_subtotal': item_subtotal,
            'dish_id': pk,
        })

    return redirect(request.META.get('HTTP_REFERER') or reverse('menu:cart'))


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    delivery_fee = Decimal(request.session.get('delivery_fee', 0))
    total_with_delivery = Decimal(cart.total()) + delivery_fee

    if request.method == 'POST':
        if not any(True for _ in cart.items()):
            messages.error(request, "Your cart is empty")
            return redirect('menu:cart')
        # include delivery info from session
        pincode = request.session.get('pincode', '')
        fee = request.session.get('delivery_fee', 0)
        # compute next sequential order number for this user
        seq = (Order.objects.filter(user=request.user)
               .aggregate(m=Max('user_order_no')).get('m') or 0) + 1
        order = Order.objects.create(
            user=request.user,
            user_order_no=seq,
            delivery_fee=fee or 0,
            delivery_pincode=pincode or ''
        )
        for item in cart.items():
            OrderItem.objects.create(
                order=order,
                dish=item['dish'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
            )
        cart.clear()
        return redirect('menu:order_summary', pk=order.pk)
    return render(request, 'menu/checkout.html', {"cart": cart,"delivery_fee": delivery_fee,
        "total_with_delivery": total_with_delivery,})


@login_required
def order_summary(request: HttpRequest, pk: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items_total = sum(item.subtotal() for item in order.items.all())
    return render(request, 'menu/order_summary.html', {"order": order, "items_total": items_total})


@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'menu/order_history.html', {"orders": orders})


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu:menu_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {"form": form})


def wishlist_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    wishlist = set(request.session.get('wishlist', []))
    key = str(pk)
    if key in wishlist:
        wishlist.remove(key)
        action = 'removed'
        message_text = "Removed from wishlist"
    else:
        wishlist.add(key)
        action = 'added'
        message_text = "Added to wishlist"
    request.session['wishlist'] = list(wishlist)
    request.session.modified = True

    # Detect AJAX requests; if AJAX, return JSON and do NOT add a Django message
    requested_with = (request.headers.get('x-requested-with') or request.META.get('HTTP_X_REQUESTED_WITH') or '')
    accept_hdr = request.META.get('HTTP_ACCEPT', '') or ''
    is_ajax = (requested_with == 'XMLHttpRequest') or ('application/json' in accept_hdr)

    if is_ajax:
        return JsonResponse({
            'status': 'ok',
            'action': action,
            'dish_id': pk,
            'wishlist': list(wishlist),
            'message': message_text,
        })

    # For non-AJAX requests, store a Django message so it appears after redirect
    if action == 'added':
        messages.success(request, message_text)
    else:
        messages.info(request, message_text)

    return redirect(request.META.get('HTTP_REFERER') or reverse('menu:menu_list'))


def wishlist_page(request: HttpRequest) -> HttpResponse:
    wishlist_ids = [int(i) for i in request.session.get('wishlist', [])]
    dishes = Dish.objects.filter(id__in=wishlist_ids, is_active=True)
    return render(request, 'menu/wishlist.html', {"dishes": dishes})


def apply_coupon(request: HttpRequest) -> HttpResponse:
    request.session['discount_pct'] = 10
    request.session.modified = True
    messages.success(request, "Coupon applied: 10% off")
    return redirect(request.META.get('HTTP_REFERER') or reverse('menu:menu_list'))


def find_promotion(request: HttpRequest) -> HttpResponse:
    messages.info(request, "Promotion found: Free delivery over ₹500")
    return redirect(request.META.get('HTTP_REFERER') or reverse('menu:menu_list'))


def set_pincode(request: HttpRequest) -> HttpResponse:
    pincode = (request.POST.get('pincode') or request.GET.get('pincode') or '').strip()
    if not pincode:
        messages.error(request, 'Please enter a pincode')
        return redirect(request.META.get('HTTP_REFERER') or reverse('menu:menu_list'))
    # match longest prefix
    zones = list(DeliveryZone.objects.all())
    match = None
    for length in range(min(6, len(pincode)), 2, -1):
        prefix = pincode[:length]
        match = next((z for z in zones if z.pincode_prefix == prefix), None)
        if match:
            break
    if match:
        request.session['pincode'] = pincode
        request.session['delivery_fee'] = float(match.fee)
        request.session['eta'] = f"{match.eta_min}-{match.eta_max} mins"
        messages.success(request, f"Delivering to {pincode}. ETA {match.eta_min}-{match.eta_max} mins. Fee ₹{match.fee}.")
    else:
        request.session['pincode'] = pincode
        request.session['delivery_fee'] = 0
        request.session['eta'] = "40-50 mins"
        messages.info(request, f"Delivering to {pincode}. Standard ETA 40-50 mins. Fee ₹0.")
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER') or reverse('menu:menu_list'))


@login_required
def pay_order(request: HttpRequest, pk: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk, user=request.user)
     # Compute subtotal (sum of item price * quantity)
    items_total = sum(item.subtotal() for item in order.items.all())
    if request.method == 'POST':
        order.status = Order.Status.PAID
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "Payment successful. Order marked as paid.")
        return redirect('menu:order_summary', pk=order.pk)
    return render(request, 'menu/payment.html', {"order": order,"items_total": items_total,})


@login_required
@require_POST
def clear_order_history(request: HttpRequest) -> HttpResponse:
    Order.objects.filter(user=request.user).delete()
    messages.info(request, "Order history cleared.")
    return redirect('menu:order_history')

