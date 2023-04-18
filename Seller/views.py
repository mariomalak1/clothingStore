from django.shortcuts import render, redirect, get_object_or_404
from Invoice.models import Cart, Order
from .forms import CreateOrderForm
from django.contrib import messages
# Create your views here.

def create_order(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            form.instance.cart = cart
            form.save()
            messages.add_message(request, messages.SUCCESS, "Order created Successfully")
            return redirect("all_orders_created", cart_code = cart_code)
    else:
        form = CreateOrderForm()
    context = {
        "form":form,
        "cart":cart,
        "page_title":"Create New Order",
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


def create_cart(request):
    cart = Cart.objects.create()
    return redirect("all_orders_created", cart.cart_code)
