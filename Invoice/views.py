from django.shortcuts import render, get_object_or_404
from .models import Cart
# Create your views here.

def check_out(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    context = {
        "cart": cart,
        "page_title":"Check Out",
    }
    return render(request, "Invoice/check_out.html", context)


