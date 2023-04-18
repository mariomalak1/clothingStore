from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart
from .forms import BuyerForm
from django.contrib import messages

# Create your views here.

def all_orders_created(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    context = {
        "cart": cart,
        "page_title":"Check Out",
    }
    return render(request, "Invoice/all_orders_created.html", context)

def check_out(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    if cart.order_set.all():
        print(cart.order_set)
        if request.method == "POST":
            buyer_form = BuyerForm(request.POST)
            if buyer_form.is_valid():
                if buyer_form.data.get("name"):
                    buyer_form.save()
                    cart.buyer = buyer_form.instance
                cart.is_finished = True
                cart.save()
                return redirect("home_page")

        buyer_form = BuyerForm()

        context = {
            "cart": cart,
            "buyer_form": buyer_form
        }
        return render(request, "Invoice/check_out.html", context)
    else:
        messages.add_message(request, messages.WARNING, "No Orders Created Yet")
        return redirect("all_orders_created", cart_code)


