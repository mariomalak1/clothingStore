from django.shortcuts import render, get_object_or_404, redirect
from Invoice.models import Cart
from django.contrib import messages

# Create your views here.

def home_page(request, cart_code = None):
    if cart_code:
        cart = Cart.objects.filter(cart_code = cart_code).first()
        print(cart)
        if cart:
            if cart.is_finished:
                messages.add_message(request, messages.WARNING, "This Is Finished Cart")
                return redirect("home_page")
    print("mario")
    context = {"cart_code":cart_code}
    return render(request, "Main/home_page.html", context)

def admin_panel(request):
    return render(request, "Main/admin_panel.html")