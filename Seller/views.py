import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import CreateOrderForm, BuyerForm, GetCartForm, UserProfile, ChangePasswordForm
from Invoice.models import Cart, Order
from .models import Branch, Site_User
from Product.models import Product as Product_Model, ProductDetail
# Create your views here.

# user must be authenticated and must have a specific branch
def create_cart(request, cart_code = None):
    seller = get_object_or_404(Site_User, id=request.user.id)
    if not cart_code or cart_code == "None":
        cart = Cart.objects.create(created_by = seller, branch=seller.branch)
    else:
        cart = Cart.objects.filter(cart_code = cart_code).first()
        if cart:
            if cart.is_finished:
                messages.add_message(request, messages.WARNING, "This Is Finished Cart, you can edit it only")
                return redirect("edit_cart", cart.cart_code)
        else:
            cart = Cart.objects.create(created_by=seller, branch=seller.branch)
    return redirect("all_orders_created", cart.cart_code)

def all_orders_created(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    orders_in_cart = cart.order_set.all().order_by("-created_at")
    context = {
        "cart": cart,
        "page_title":"Check Out",
        "cart_code": cart_code,
        "orders_in_cart":orders_in_cart,
    }
    return render(request, "Seller/all_orders_created.html", context)

# user must be authenticated
# create this function to get the sizes of specific product that user choose it while he makes an order
def get_sizes(request):
    product_id = request.GET.get('product_id', None)  # Extract product_id from request.GET
    if product_id is None:
        return JsonResponse({'error': 'Product ID not found in request.'})  # Handle error
    product = get_object_or_404(Product_Model, id=product_id)
    sizes = product.product_detail.sizes.all()
    list_of_sizes = []
    for size in sizes:
        dic = {"size_name": size.name, "size_id": size.id}
        list_of_sizes.append(dic)
    response_data = {'sizes': list_of_sizes}
    return JsonResponse(response_data)

# user must be authenticated and must have a specific branch
def create_order(request, cart_code):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    seller = get_object_or_404(Site_User, id = request.user.id)
    branch = get_object_or_404(Branch, id = seller.branch_id)
    if request.method == "POST":
        form = CreateOrderForm(branch, request.POST)
        if form.is_valid():
            order = form.instance
            order.cart = cart
            # decrease the product quantity in the branch the order created in
            order.product.quantity -= order.quantity
            order.product.save()
            form.save()
            messages.add_message(request, messages.SUCCESS, "Order created Successfully")
            if cart.is_finished:
                return redirect("edit_cart", cart_code = cart_code)
            else:
                return redirect("all_orders_created", cart_code = cart_code)
    else:
        form = CreateOrderForm(branch)
    context = {
        "form":form,
        "cart":cart,
        "page_title":"Create New Order",
        "cart_code":cart_code,
        }
    return render(request, "Seller/create_order.html", context)


# user must be authenticated and must have a specific branch
def delete_order(request, order_id, order_number):
    order = get_object_or_404(Order, id = order_id)

    if request.method == "POST":
        # increase the product quantity in the branch the order created in
        order.product.quantity += order.quantity
        order.product.save()
        Order.delete(order)
        messages.add_message(request, messages.SUCCESS, "Order delete Successfully")
        return redirect("all_orders_created", order.cart.cart_code)

    context = {"object_name": f"order {order_number}",
               "afterObjName":f'With Total Cost "{order.total_cost_for_order()}"',
               "cart_code": order.cart.cart_code,
               "anotherText": f"Quantity : {order.quantity}",
               }
    return render(request, "delete_confirmation.html", context)

# user must be authenticated and must have a specific branch
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

## function to delete the cart and return specific endpoint to redirect user to it
def delete_cart_function(request, cart, place):
    for order_ in cart.order_set.all():
        order_.product.quantity += order_.quantity
        order_.product.save()
    Cart.delete(cart)
    messages.add_message(request, messages.SUCCESS, "Cart delete Successfully")
    if place:
        if place == "AllCarts":
            return ("display_all_carts")
        ## if he's seller and make refund, or admin, but he come from refund from specific branch, will redirect him to home page
    return ("home_page")

# must user be authenticated
# place is parameter that I will redirect him to place he come from
def delete_cart(request, cart_code, place = None):
    cart = get_object_or_404(Cart, cart_code = cart_code)
    total = 0
    if request.method == "GET":
        if cart.order_set.count() == 0:
            return redirect( delete_cart_function(request, cart, place) )
        else:
            total = cart.total_price()
    if request.method == "POST":
        return redirect( delete_cart_function(request, cart, place) )
    print(place)
    context = {"object_name": f"Cart",
               "afterObjName":f'With Total Cost "{total}"',
               "anotherText": f"With Number Orders : {cart.order_set.count()}",
               "cart_code":cart_code,
               "cancel_redirect": place
               }
    return render(request, "delete_confirmation.html", context)

# user must be authenticated and must have a specific branch
def get_cart_code_from_user(request):
    if request.method == "POST":
        form = GetCartForm(request.POST)
        cart_code = form.data.get("cart_code").strip()
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
    orders_in_cart = cart.order_set.all().order_by("-created_at")
    if cart.is_finished:
        cart.edit_at = datetime.datetime.now()
        context = {
            "cart": cart,
            "page_title":"Edit Cart",
            "cart_code":cart_code,
            "orders_in_cart": orders_in_cart,
        }
        return render(request, "Seller/all_orders_created.html", context)
    else:
        messages.add_message(request, messages.WARNING, "This not Completed Cart, You Can Enter it Again from Sale and Complete it")
        return redirect("home_page", cart_code = cart_code)

def check_out_exchange(request, old_cart_code):
    context = {"cart_code":old_cart_code}
    return render(request, "Seller/check_out_exchange.html", context)

def user_profile(request):
    user_ = get_object_or_404(Site_User, id = request.user.id)
    if request.method == "POST":
        if user_.user_type == 0:
            form = UserProfile(request.POST, instance=user_)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data Saved")
                return redirect("admin_panel")
        else:
            messages.add_message(request, messages.WARNING, "You Can't Change This Data")
            return redirect("home_page")
    else:
        form = UserProfile(instance=user_)
    context = {
        "form":form,
        "current_user":user_,
    }
    return render(request, "Seller/user_profile.html", context)

def change_password(request):
    user_ = get_object_or_404(Site_User, id = request.user.id)
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            new_password = form.cleaned_data.get("new_password1")
            if user_.check_password(old_password):
                user_.set_password(new_password)
                user_.save()
                messages.add_message(request, messages.SUCCESS, "Password Changed Successfully")
                return redirect("login")
            else:
                messages.add_message(request, messages.ERROR, "Old Password is InValid, Enter Valid One")
                return redirect("change_password")
    else:
        form = ChangePasswordForm()
    context = {
        "form":form,
        "current_user":user_,
    }
    return render(request, "Seller/change_password.html", context)