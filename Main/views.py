from django.shortcuts import render, get_object_or_404, redirect
from Invoice.models import Cart
from django.contrib import messages
from Seller.models import Seller as Seller_Model
from AdminPanel.decorators import is_authenticated_admin_decorator

# Create your views here.
def home_page(request, cart_code=None):
    seller = get_object_or_404(Seller_Model, id=request.user.id)
    context = {"seller": seller}
    if cart_code:
        cart = Cart.objects.filter(cart_code=cart_code).first()
        if cart:
            context["cart_code"] = cart_code
            return render(request, "Main/home_page.html", context)
        else:
            messages.add_message(request, messages.WARNING, "No Card Found with This Code")
            return render(request, "Main/home_page.html", context)
    else:
        return render(request, "Main/home_page.html", context)

@is_authenticated_admin_decorator
def admin_panel(request):
    return render(request, "Main/admin_panel.html", {"page_title": "Admin Panel", "user":request.user})

@is_authenticated_admin_decorator
def settings(request):
    return render(request, "Main/settings.html")