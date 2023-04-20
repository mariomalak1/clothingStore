from django.shortcuts import render, redirect, get_object_or_404
from Invoice.models import Cart, Order
from .forms import CreateOrderForm, BuyerForm, GetCartForm
from django.contrib import messages
import datetime
# Create your views here.

def create_cart(request, cart_code = None):
    if not cart_code or cart_code == "None":
        cart = Cart.objects.create()
        print("mario")
    else:
        cart = Cart.objects.filter(cart_code = cart_code).first()
        if cart:
            if cart.is_finished:
                messages.add_message(request, messages.WARNING, "This Is Finished Cart, you can edit it only")
                return redirect("edit_cart", cart.cart_code)
        else:
            cart = Cart.objects.create()
    return redirect("all_orders_created", cart.cart_code)

def all_orders_created(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    context = {
        "cart": cart,
        "page_title":"Check Out",
        "cart_code": cart_code,
    }
    return render(request, "Seller/all_orders_created.html", context)

def create_order(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            form.instance.cart = cart
            form.save()
            messages.add_message(request, messages.SUCCESS, "Order created Successfully")
            if cart.is_finished:
                return redirect("edit_cart", cart_code = cart_code)
            else:
                return redirect("all_orders_created", cart_code = cart_code)
    else:
        form = CreateOrderForm()
    context = {
        "form":form,
        "cart":cart,
        "page_title":"Create New Order",
        "cart_code":cart_code,
        }
    return render(request, "Seller/create_order.html", context)

def delete_order(request, order_id, order_number):
    order = get_object_or_404(Order, id = order_id)

    if request.method == "POST":
        Order.delete(order)
        messages.add_message(request, messages.SUCCESS, "Order delete Successfully")
        return redirect("all_orders_created", order.cart.cart_code)

    context = {"object_name": f"order {order_number}",
               "afterObjName":f'With Total Cost "{order.total_for_order()}"',
               "cart_code": order.cart.cart_code,
               "anotherText": f"Quantity : {order.quantity}, Size : {order.product.size}",
               }
    return render(request, "Seller/delete_confirmation.html", context)

def check_out(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    if not cart.is_finished:
        if cart.order_set.all():
            if request.method == "POST":
                buyer_form = BuyerForm(request.POST)
                if buyer_form.is_valid():
                    if buyer_form.data.get("name"):
                        buyer_form.save()
                        cart.buyer = buyer_form.instance
                    cart.is_finished = True
                    cart.save()
                    messages.add_message(request,messages.SUCCESS, f"Check Out For Cart with Code {cart.cart_code} is Finished Successfully")
                    return redirect("home_page")

            buyer_form = BuyerForm()

            context = {
                "cart": cart,
                "buyer_form": buyer_form,
                "cart_code": cart_code,
            }
            return render(request, "Seller/check_out.html", context)
        else:
            messages.add_message(request, messages.WARNING, "No Orders Created Yet")
            return redirect("all_orders_created", cart_code)
    else:
        messages.add_message(request, messages.WARNING, "this complete Cart, You can Edit in This Page")
        return redirect("edit_cart", cart_code)

def delete_cart(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)

    if cart.order_set.all():
        total = cart.total_price()
    else:
        messages.add_message(request, messages.WARNING, "Cart Has No Orders Yet")
        return redirect("all_orders_created", cart.cart_code)
    if request.method == "POST":
        Cart.delete(cart)
        messages.add_message(request, messages.SUCCESS, "Cart delete Successfully")
        return redirect("home_page")

    context = {"object_name": f"Cart",
               "afterObjName":f'With Total Cost "{total}"',
               "anotherText": f"With Number Orders : {cart.order_set.count()}",
               "cart_code":cart_code
               }
    return render(request, "Seller/delete_confirmation.html", context)

def get_cart_code_from_user(request):
    if request.method == "POST":
        form = GetCartForm(request.POST)
        cart_code = form.data.get("cart_code")
        cart = Cart.objects.filter(cart_code=cart_code).first()
        if cart:
            return redirect("edit_cart", cart_code = cart.cart_code)
        else:
            messages.add_message(request, messages.WARNING, "No Cart Found with This Code")
            return redirect("get_cart_code_from_user")
    else:
        form = GetCartForm()

    context = {"form":form}
    return render(request, "Seller/get_cart_code_from_user.html", context)

def edit_cart(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    if cart.is_finished:
        cart.edit_at = datetime.datetime.now()
        context = {
            "cart": cart,
            "page_title":"Edit Cart",
            "cart_code":cart_code,
        }
        return render(request, "Seller/all_orders_created.html", context)
    else:
        messages.add_message(request, messages.WARNING, "This not Completed Cart, You Can Enter it Again from Sale and Complete it")
        return redirect("home_page", cart_code = cart_code)

def check_out_exchange(request, old_cart_code):
    context = {"cart_code":old_cart_code}
    return render(request, "Seller/check_out_exchange.html", context)
