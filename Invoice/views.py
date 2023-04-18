from django.shortcuts import render, get_object_or_404
from .models import Cart
# Create your views here.

def all_in_cart(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    context = {
        "code": cart.cart_code,
        "total": cart.total_price(),
        "orders_in_cart": cart.order_set.all(),
        "delete_label": "Delete Order Confirmation",
        "delete_message": "you sure that you want to delete this order ?",

    }
    return render(request, "Invoice/all_in_cart.html", context)
