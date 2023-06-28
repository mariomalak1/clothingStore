from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from AdminPanel.decorators import *
from Seller.models import Branch, Site_User
from .forms import AddProductInBranchForm
from .models import Product as Product_Model
# Create your views here.

@is_authenticated_seller_decorator
def add_product_in_branch(request, branch_id):
    branch = get_object_or_404(Branch, id = branch_id)
    seller = get_object_or_404(Site_User, id = request.user.id)
    if seller.branch == branch:
        if request.method == "POST":
            form = AddProductInBranchForm(request.POST)
            if form.is_valid():
                product_ = form.instance
                product_.branch = branch
                if product_.product_detail.price == 0 and product_.price_for_branch == 0:
                    messages.add_message(request, messages.WARNING, "Note That The Price For The Product you Choose Is 0 And You Enter 0 For It's Price In Your Branch !!!")
                elif product_.price_for_branch == 0:
                    product_.price_for_branch = product_.product_detail.price

                # show if found in the branch the same product, to add to it the new quantity he wants to add
                another_product_with_same_data = Product_Model.objects.filter(product_detail = product_.product_detail, price_for_branch = product_.price_for_branch, branch = product_.branch).first()
                if another_product_with_same_data:
                    another_product_with_same_data.quantity += product_.quantity
                    another_product_with_same_data.save()
                    messages.add_message(request, messages.SUCCESS, f"Product Of Code {product_.product_detail.product_code} Add Successfully To The Old Stuff")
                else:
                    form.save()
                    messages.add_message(request, messages.SUCCESS, f"Product Of Code {product_.product_detail.product_code} Add Successfully")
                return redirect("add_product_in_branch", branch.id)
        else:
            form = AddProductInBranchForm()
        context = {
            "form":form,
            "branch": branch,
            "process_name":"Add",
            "button_name":"Add",
        }
        return render(request, "Product/add_product_in_branch.html", context)
    else:
        messages.add_message(request, messages.WARNING, "This Not Your Branch To Add Product In!!")
        return redirect("home_page")

@is_authenticated_seller_decorator
def display_all_products_in_branch(request, branch_id):
    branch = get_object_or_404(Branch, id = branch_id)
    products = Product_Model.objects.filter(branch=branch).all()
    context = {
        "products":products,
        "branch":branch,
    }
    return render(request, "Product/display_all_products_in_branch.html", context)

@is_authenticated_admin_or_manager_decorator
def edit_product_in_branch(request, branch_id, product_id):
    pass

@is_authenticated_admin_or_manager_decorator
def delete_product_in_branch(request, branch_id, product_id):
    pass