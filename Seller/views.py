from django.shortcuts import render, redirect, get_object_or_404
from Invoice.models import Cart, Order
from .forms import CreateOrderForm, BuyerForm, GetCartForm, AddUserForm, AddSellerForm, AddNewBranch
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Seller, Branch
import datetime
# Create your views here.

def create_cart(request, cart_code = None):
    if not cart_code or cart_code == "None":
        seller = get_object_or_404(Seller, user_obj = request.user)
        cart = Cart.objects.create(created_by = seller)
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
    return render(request, "delete_confirmation.html", context)

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
    return render(request, "delete_confirmation.html", context)

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


# admin views
def add_new_user(request):
    if request.method == "POST":
        form_user = AddUserForm(request.POST)
        form_seller = AddSellerForm(request.POST)
        if form_seller.is_valid() and form_user.is_valid():
            form_user.save()
            form_seller.instance.user = form_user.instance
            if form_seller.data.get("is_admin"):
                form_user.instance.is_staff = True
            form_user.save()
            form_seller.save()
            username = form_user.cleaned_data.get("username")
            messages.success(request, f"Seller with Username {username} have been created")
            return redirect("admin_panel")
    else:
        form_user = AddUserForm()
        form_seller = AddSellerForm()

    context = {"form_user":form_user, "form_seller":form_seller}
    return render(request, "Seller/User/register.html", context)

def add_new_branch(request):
    if request.method == "POST":
        form = AddNewBranch(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Congratulations, Branch Successfully Opened In System, You Can Add To It Sellers and Managers from Admin Panel")
            return redirect("display_all_branches")
    else:
        form = AddNewBranch()
    return render(request, "Seller/add_new_branch.html",{"form":form, "process_name":"Open", "button_name":"Create"})

def display_all_branches(request):
    branches = Branch.objects.all()
    context = {"branches":branches}
    return render(request, "Seller/display_all_branches.html", context)

def edit_product_detail(request, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    if request.method == "POST":
        form = AddNewBranch(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, f"Branch With Name {branch_name} Edited Successfully")
            branch.name = form.cleaned_data.get("name")
            branch.address = form.cleaned_data.get("address")
            branch.phone_branch = form.cleaned_data.get("phone_branch")
            branch.save()
            return redirect("display_all_branches")
    else:
        form = AddNewBranch(instance=branch)
    context = {"process_name":"Edit", "form":form, "button_name":"Save"}
    return render(request, "Seller/add_new_branch.html",context)

def delete_branch(request, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    if request.method == "POST":
        branch.delete()
        messages.add_message(request, messages.SUCCESS, f"Branch With Name {branch_name} Successfully Deleted")
        return redirect("display_all_branches")
    else:
        total_number_of_employees = branch.seller_set.count()
        total_number_of_products = 0
        for product_branch in branch.product_set.all():
            total_number_of_products += product_branch.quantity

        context = {"branch":branch, "total_number_of_employees":total_number_of_employees, "total_number_of_products":total_number_of_products}
        return render(request, "Seller/branch_delete_confirmation.html", context)
