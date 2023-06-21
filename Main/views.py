from django.shortcuts import render, get_object_or_404, redirect
from Invoice.models import Cart
from django.contrib import messages
from Seller.models import User
from AdminPanel.decorators import is_authenticated_admin_decorator, is_authenticated_seller_decorator, is_authenticated_admin_or_manager_decorator

# Create your views here.
@is_authenticated_seller_decorator
def home_page(request, cart_code=None):
    user = get_object_or_404(User, id=request.user.id)
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

@is_authenticated_admin_or_manager_decorator
def admin_panel(request):
    if request.user.is_staff:
        page_title = "Admin Panel"
    else:
        page_title = "Manager Panel"

    context = {
        "page_title": page_title,
        "user":request.user,
    }
    return render(request, "Main/admin_panel.html", )

@is_authenticated_admin_decorator
def settings(request):
    if request.method == "POST":
        pass
    else:
        pass
    return render(request, "Main/settings.html")