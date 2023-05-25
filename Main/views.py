from django.shortcuts import render, get_object_or_404, redirect
from Invoice.models import Cart
from django.contrib import messages
from Seller.models import Seller as Seller_Model


# Create your views here.

def home_page(request, cart_code=None):
    try:
        seller = Seller_Model.objects.get(request.user.id)
        if seller:
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
        else:
            messages.add_message(request, messages.WARNING, "Please Login")
            return redirect("login")
    except:
        return redirect("login")


def admin_panel(request):
    return render(request, "Main/admin_panel.html", {"page_title": "Admin Panel"})
