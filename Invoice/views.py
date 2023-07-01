from django.shortcuts import render
from django.http import Http404
from Invoice.models import Cart
# create views here.

def create_invoice(request, cart_code):
    cart_ = Cart.objects.filter(cart_code=cart_code).first()
    if cart_:
        context = {
            "cart":cart_,
        }
        return render(request, "Invoice/invoice.html", context)
    else:
        return Http404()