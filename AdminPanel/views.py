from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest
##################
from .forms import AddSellerForm, AddNewBranch, EditBranchForm, EditUserForm
from .filters import CartFilter, CartFilterForManager
from Invoice.models import Cart, Order
from Seller.models import Branch, Site_User
from .decorators import *
# Create your views here.

@is_authenticated_admin_or_manager_decorator
def display_all_carts(request):
    user_ = get_object_or_404(Site_User, id = request.user.id)
    total_money_entered = 0
    if user_.is_site_admin():
        carts = Cart.objects.all().order_by('-created_at')
        cart_filter = CartFilter(data= request.GET, queryset=carts)
    else:
        carts = Cart.objects.filter(branch=user_.branch).order_by('-created_at')
        cart_filter = CartFilterForManager(data= request.GET, queryset=carts)
    for cart in cart_filter.qs:
        total_money_entered += cart.total_price()
    context = {
        "carts":cart_filter.qs,
        "total_money_entered": total_money_entered,
        "cart_filter":cart_filter,
        "number_of_carts":cart_filter.qs.count(),
        "user_site":user_,
    }
    return render(request, "AdminPanel/display_all_carts.html", context)

@is_authenticated_admin_decorator
def add_new_user(request):
    if request.method == "POST":
        form_seller = AddSellerForm(request.POST)
        if form_seller.is_valid():
            username = form_seller.cleaned_data.get("username")
            user_type = form_seller.cleaned_data.get("user_type")
            form_seller.save()
            messages.success(request, f"{Site_User.USER_TYPE_CHOICES[int(user_type)][1]} with Username {username} have been created")
            return redirect("display_all_users")
    else:
        form_seller = AddSellerForm()

    context = {"form_seller":form_seller}
    return render(request, "AdminPanel/register.html", context)

@is_authenticated_admin_decorator
def display_all_users(request):
    users = Site_User.objects.all().order_by("user_type", "-salary")
    current_user = get_object_or_404(Site_User, id=request.user.id)
    context = {
        "users":users,
        "current_user":current_user,
    }
    return render(request, "AdminPanel/display_all_users.html", context)

@is_authenticated_admin_decorator
def get_user(request, user_id):
    user_ = get_object_or_404(Site_User, id = user_id)
    user_request = get_object_or_404(Site_User, id = request.user.id)
    if user_request.is_superuser or (not user_.is_staff and user_request.user_type == 0):
        if request.method == "POST":
            form = EditUserForm(request.POST, instance=user_)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "User Saved Successfully")
                return redirect("display_all_users")
        else:
            form = EditUserForm(instance=user_)
        context = {
            "user_id": user_id,
            "form": form,
        }
        return render(request, "AdminPanel/specific_user.html", context)
    else:
        return HttpResponseForbidden()

@is_authenticated_admin_decorator
def delete_user(request, user_id):
    user_to_deleted = get_object_or_404(Site_User, id = user_id)
    user_request = get_object_or_404(Site_User, id = request.user.id)
    delete_condition = False
    ## superuser can delete anyone
    if user_request.is_superuser:
        delete_condition = True
    ## if user delete is admin and the user that will delete not an admin
    elif user_request.user_type == 0 and (user_to_deleted.user_type > 0):
        delete_condition = True
    ## if user try to delete him self
    elif user_request == user_to_deleted:
        messages.add_message(request, messages.WARNING, "You can't Edit This User")
        return redirect("get_user", user_id)
    else:
        messages.add_message(request, messages.WARNING, "You can't Edit This User")
        return redirect("get_user", user_id)

    if delete_condition:
        if request.method == "POST":
            for cart in user_to_deleted.cart_set.all():
                cart.created_by = user_request
                cart.save()
            user_to_deleted.delete()
            messages.add_message(request, messages.SUCCESS, "User Deleted Successfully")
            return redirect("display_all_users")
        context = {
            "deleted_user": user_to_deleted,
        }
        return render(request, "AdminPanel/user_delete_confirmation.html", context)
    else:
        messages.add_message(request, messages.WARNING, "You can't Edit This User")
        return redirect("get_user", user_id)

@is_authenticated_admin_decorator
def add_new_branch(request):
    if request.method == "POST":
        form = AddNewBranch(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Congratulations, Branch Successfully Opened In System, You Can Add To It Sellers and Managers from Admin Panel")
            return redirect("display_all_branches")
    else:
        form = AddNewBranch()
    return render(request, "AdminPanel/add_new_branch.html", {"form":form, "process_name": "Open", "button_name": "Create"})

@is_authenticated_admin_decorator
def display_all_branches(request):
    branches = Branch.objects.all()
    context = {"branches":branches}
    return render(request, "AdminPanel/display_all_branches.html", context)

@is_authenticated_admin_decorator
def save_branch_data(form, branch, request):
    branch_name = branch.name
    branch.name = form.cleaned_data.get("branch")
    branch.address = form.cleaned_data.get("address")
    branch.phone_branch = form.cleaned_data.get("phone_branch")
    branch.save()
    messages.add_message(request, messages.SUCCESS,
                         f"Branch With Name {branch_name} Edited Successfully To {branch.name}")

@is_authenticated_admin_decorator
def edit_branch(request, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    if request.method == "POST":
        form = EditBranchForm(request.POST)
        if form.is_valid():
            try:
                branch_form = Branch.objects.filter(name = form.cleaned_data.get("branch")).first()
                if branch_form:
                    if branch_form == branch:
                        save_branch_data(form, branch, request)
                    else:
                        messages.add_message(request, messages.WARNING,
                                             f"There's Another Branch With Same Name")
                else:
                    save_branch_data(form, branch, request)
            except:
                save_branch_data(form, branch, request)
            return redirect("display_all_branches")
    else:
        form = EditBranchForm(instance=branch)
        form["branch"].initial = branch.name
    context = {"process_name":"Edit", "form":form, "button_name":"Save"}
    return render(request, "AdminPanel/add_new_branch.html", context)

@is_authenticated_admin_decorator
def delete_branch(request, branch_name):
    branch = get_object_or_404(Branch, name=branch_name)
    if request.method == "POST":
        branch.delete()
        messages.add_message(request, messages.SUCCESS, f"Branch With Name {branch_name} Successfully Deleted")
        return redirect("display_all_branches")
    else:
        total_number_of_employees = branch.site_user_set.count()
        total_number_of_products = 0
        for product_branch in branch.product_set.all():
            total_number_of_products += product_branch.quantity

        context = {"branch":branch, "total_number_of_employees":total_number_of_employees, "total_number_of_products":total_number_of_products}
        return render(request, "AdminPanel/branch_delete_confirmation.html", context)

@is_authenticated_admin_or_manager_decorator
def show_statistics(request):
    user_ = get_object_or_404(Site_User, id = request.user.id)
    context = {
        "user_site": user_,
    }
    return render(request, "AdminPanel/show_statistics.html", context)